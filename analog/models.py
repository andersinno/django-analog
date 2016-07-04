from __future__ import unicode_literals

from analog.exceptions import UnknownLogKind
from analog.settings import KIND_LABELS, KINDS, KIND_IDS
from django.conf import settings
from django.db import models
from django.utils.encoding import force_text
from django.utils.six import string_types, integer_types
from jsonfield import JSONField


def _map_kind(kind):
    if isinstance(kind, string_types):
        if kind not in KINDS:
            raise UnknownLogKind(kind)
        kind = KINDS[kind]
    assert isinstance(kind, integer_types)
    if kind not in KIND_IDS:
        raise UnknownLogKind(kind)
    return kind


class BaseLogEntry(models.Model):
    """
    Abstract base model class for the various log models.

    The concrete models are created by :func:`define_log_model`.

    In addition, directly deriving a model from `BaseLogEntry` is supported
    (for instance, to allow for log entries that are not attached to other
    models), though the `add_log_entry` function will naturally not be
    automatically augmented to pass a `target` parameter.
    """

    target = None  # This will be overridden dynamically
    created_on = models.DateTimeField(auto_now_add=True, editable=False)
    user = models.ForeignKey(
        getattr(settings, "AUTH_USER_MODEL", "auth.User"),
        null=True, on_delete=models.PROTECT
    )
    message = models.CharField(max_length=256)
    identifier = models.CharField(max_length=64, blank=True)
    kind = models.IntegerField(default=0, db_index=True)
    extra = JSONField(null=True, blank=True)

    class Meta:
        abstract = True

    def get_kind_display(self):
        """
        Get the kind label for this log entry.

        This emulates the behavior Django would have for fields that
        have the ``choices`` kwarg.
        """
        return KIND_LABELS.get(self.kind, self.kind)

    def save(self, *args, **kwargs):
        if self.pk:
            raise ValueError("%r objects may not be modified" % self.__class__)
        super(BaseLogEntry, self).save(*args, **kwargs)

    @classmethod
    def add_log_entry(
        cls,
        target, message, identifier=None, kind="other",
        user=None, extra=None, save=True,
        **kwargs
    ):
        """
        Add a log entry.

        .. note::

           This method should not be used directly; instead, the same method,
           aside from the `target` argument, is available on models that
           have been anointed by :func:`define_log_model`.

        :param target: Target model instance
        :param message: Log message
        :type message: str
        :param identifier: Log message identifier.
                           Useful for tagging log entries in a way that is
                           not necessarily human-readable.
        :type identifier: str|None
        :param kind: Log entry kind. Either a mnemonic string (preferred and
                     readable), or the actual entry ID integer (if you really
                     have to). Kinds are configured in your project's settings.
        :type kind: int|str
        :param user: An optional user object (an instance of
                     ``settings.AUTH_USER_MODEL``) to attach to this log entry.
        :param extra: Extra data, if applicable. If set, this must be
                      serializable to JSON; ``dict``s are a good idea.
        :type extra: object|None
        :param kwargs: Any other fields to pass to the constructor of the
                       class. Mainly useful with log classes derived from
                       `BaseLogEntry`.
        :type kwargs: dict
        :param save: Whether to immediately save the log entry. Default True.
        :type save: bool
        :return: The created log entry
        """

        if target is not None and not getattr(target, "pk", None):
            raise ValueError("Can not create log entry for unsaved object")

        kind = _map_kind(kind)

        if not getattr(user, "pk", None):
            user = None

        kwargs = dict(
            target=target,
            message=message,
            identifier=force_text(identifier or "", errors="ignore")[:64],
            user=user,
            kind=kind,
            extra=(extra or None),
            **kwargs
        )
        if target is None:
            kwargs.pop('target')
        log_entry = cls(**kwargs)
        log_entry.clean()
        if save:
            log_entry.save()
        return log_entry
