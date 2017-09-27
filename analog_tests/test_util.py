import pytest

from analog.exceptions import UnknownLogKind
from analog.util import LogEntryKindMap


def test_known():
    kind_map = LogEntryKindMap()
    assert kind_map.OTHER == 0
    assert kind_map.NOTE == 4
    assert kind_map.ERROR == 7


def test_unknown():
    kind_map = LogEntryKindMap()
    with pytest.raises(UnknownLogKind):
        kind_map.UNKNOWN_KIND


def test_internal():
    kind_map = LogEntryKindMap()
    assert kind_map.__module__ == 'analog.util'
    assert LogEntryKindMap.__module__ == 'analog.util'


def test_internal_attribute_error():
    kind_map = LogEntryKindMap()
    with pytest.raises(AttributeError) as excinfo:
        kind_map.__wrapped__
    assert str(excinfo.value) == (
        "'LogEntryKindMap' object has no attribute '__wrapped__'")
