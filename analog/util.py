from analog.exceptions import UnknownLogKind
from analog.settings import KINDS


class LogEntryKindMap(object):
    """
    A helper class for transitioning old code.

    Allows looking up log entry kinds by "enumish" name, i.e.
    ``LogEntryKind.OTHER`` would map to the "other" kind's ID.
    """

    def __getattr__(self, kind):
        """
        Get the kind ID for the given kind mnemonic.

        :param kind: Kind mnemonic.
        :type kind: str
        :return: int
        """
        kind = str(kind).lower()
        if kind not in KINDS:
            raise UnknownLogKind(kind)
        return KINDS[kind]
