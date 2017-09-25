from .define import define_log_model  # noqa
from .models import BaseLogEntry
from .util import LogEntryKindMap

LogEntryKind = LogEntryKindMap()

__all__ = ("define_log_model", "LogEntryKind", "BaseLogEntry")
