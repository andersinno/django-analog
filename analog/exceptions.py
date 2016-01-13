class UnknownLogKind(ValueError):
    """Exception thrown when an unknown ``kind`` is passed."""

    def __init__(self, value):
        """
        Construct the exception.

        :param value: The invalid kind value passed in.
        """
        message = "Unknown log entry kind %r" % value
        super(UnknownLogKind, self).__init__(message)
