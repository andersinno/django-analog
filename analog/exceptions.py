class UnknownLogKind(ValueError):
    """Exception thrown when an unknown ``kind`` is passed."""

    def __init__(self, value):
        """
        Construct the exception.

        :param value: The invalid kind value passed in.
        """
        message = "Unknown log entry kind %r" % value
        super().__init__(message)


class NoExtraField(ValueError):
    pass
