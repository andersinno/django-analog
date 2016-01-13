from .util import LogEntryKindMap
from .define import define_log_model  # noqa
from .models import BaseLogEntry

LogEntryKind = LogEntryKindMap()

__all__ = ("define_log_model", "LogEntryKind", "BaseLogEntry")
