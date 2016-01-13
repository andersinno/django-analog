from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from django.utils.six import string_types

_DEFAULT_KINDS = {
    "other": 0,
    "audit": 1,
    "edit": 2,
    "deletion": 3,
    "note": 4,
    "email": 5,
    "warning": 6,
    "error": 7
}

_DEFAULT_KIND_LABELS = {
    "other": _("other"),
    "audit": _("audit"),
    "edit": _("edit"),
    "deletion": _("deletion"),
    "note": _("note"),
    "email": _("email"),
    "warning": _("warning"),
    "error": _("error")
}


def _get_kind_labels(kinds):
    kind_labels = _DEFAULT_KIND_LABELS.copy()
    kind_labels.update(getattr(settings, "ANALOG_KIND_LABELS", {}))
    kind_labels = dict(
        (KINDS.get(mnemonic, mnemonic), label)
        for (mnemonic, label) in kind_labels.items()
    )
    for key in list(kind_labels):
        if isinstance(kind_labels[key], string_types):
            kind_labels[key] = _(kind_labels[key])
    return kind_labels


#: A mapping from kind mnemonic (string) to kind ID (integer)
KINDS = _DEFAULT_KINDS.copy()
KINDS.update(getattr(settings, "ANALOG_KINDS", {}))

#: A mapping from kind ID (integer) to label
KIND_LABELS = _get_kind_labels(KINDS)

KIND_IDS = set(KINDS.values())
