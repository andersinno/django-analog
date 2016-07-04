from django.db import models
from .models import BaseLogEntry

all_known_log_models = {}


def define_log_model(
    model_class,
    base_class=BaseLogEntry,
    on_delete=models.CASCADE
):
    """
    Define a log model for a given Django model class ("parent model").

    The log entry model class is returned, and it must be assigned to
    a variable in a `models.py` file to allow Django to pick it up
    for migrations.

    For all intents and purposes, the log entry model is owned by your
    app after this function creates it.

    The parent model is anointed with two new attributes:

    * ``add_log_entry``, a function to add a log entry. (See
      :func:`BaseLogEntry.add_log_entry` for details,
      but heed the fact that the ``target`` argument will be
      implicitly passed.)
    * ``log_model``, a reference to the log entry model.

    :param model_class: The model class this log entry model is for.
    :param base_class: Replacement base class for the model. Should
                       be compatible with :class:`BaseLogEntry` never-
                       theless.
    :param on_delete: The `on_delete` clause for the log entry class's
                      foreign key. Defaults to `CASCADE`, i.e. that
                      log entries are deleted when the logged model
                      instance is.  `PROTECT` would be another sane
                      option.
    :return: The log entry model.
    """
    log_model_name = "%sLogEntry" % model_class.__name__

    class Meta:
        app_label = model_class._meta.app_label
        abstract = False

    class_dict = {
        "target": models.ForeignKey(
            model_class,
            related_name="log_entries",
            on_delete=on_delete
        ),
        "__module__": model_class.__module__,
        "Meta": Meta,
        "logged_model": model_class,
    }

    log_entry_class = type(str(log_model_name), (base_class,), class_dict)

    def add_log_entry(
        self, message, identifier=None, kind="other",
        user=None, extra=None, save=True, **kwargs
    ):
        return log_entry_class.add_log_entry(
            target=self,
            message=message,
            identifier=identifier,
            kind=kind,
            user=user,
            extra=extra,
            save=save,
            **kwargs
        )

    setattr(model_class, "add_log_entry", add_log_entry)
    setattr(model_class, "log_model", log_entry_class)
    all_known_log_models[model_class] = log_entry_class
    return log_entry_class
