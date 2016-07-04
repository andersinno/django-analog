import pytest
from analog import define_log_model, LogEntryKind, BaseLogEntry
from analog.exceptions import UnknownLogKind
from analog_tests.models import LoggedModel, LoggedModelLogEntry, FreeLogEntry
from django.db import models


class RandomModel(models.Model):
    pass


def qs_last(qs):  # Compatibility shim for old Djangos
    try:
        return qs.last()
    except AttributeError:
        return list(qs.all())[-1]


@pytest.fixture(scope="module", params=["free", "target"])
def target_object(request):
    if request.param == "target":
        return LoggedModel.objects.create()
    else:
        class FakeModel:
            pk = None

            def add_log_entry(self, **kwargs):
                return FreeLogEntry.add_log_entry(target=None, **kwargs)

            log_entries = FreeLogEntry.objects.all()

        return FakeModel()


def test_model_sanity():
    RandomModelLogEntry = define_log_model(RandomModel)
    assert RandomModelLogEntry.__module__ == RandomModel.__module__
    assert RandomModelLogEntry._meta.get_field("target").rel.to is RandomModel
    try:
        rel = RandomModel.log_entries.related
        # TODO: Assert here too?
    except AttributeError:  # Django 1.9+
        rel = RandomModel.log_entries.rel
        assert rel.model is RandomModel
        assert rel.related_model is RandomModelLogEntry

    assert issubclass(RandomModelLogEntry, BaseLogEntry)
    assert isinstance(RandomModelLogEntry(), BaseLogEntry)


@pytest.mark.django_db
@pytest.mark.parametrize("kwarg", (False, True), ids=('args', 'kwargs'))
def test_add_log_entry(target_object, kwarg):
    if target_object.pk:
        # yigh, for some reason I don't care to look into more deeply (you
        # know what they say about abysses), Django 1.4 sometimes hasn't
        # actually saved this object correctly. So save it again just in case.
        target_object.save()

    if kwarg:
        target_object.add_log_entry(message="hello, world")
    else:
        if not target_object.pk:
            pytest.skip('free log entries do not support kwargless api')
        target_object.add_log_entry("hello, world")
    assert target_object.log_entries.count() == 1
    log_entry = qs_last(target_object.log_entries)
    if log_entry.target:
        assert isinstance(log_entry, LoggedModelLogEntry)
    assert isinstance(log_entry, BaseLogEntry)


@pytest.mark.django_db
def test_log_entry_kind(target_object):
    target_object.add_log_entry(message="edited", kind=LogEntryKind.EDIT)
    log_entry = qs_last(target_object.log_entries)
    assert log_entry.get_kind_display() == "edit"


@pytest.mark.django_db
def test_log_mutation(target_object):
    target_object.add_log_entry(message="benign action", kind=LogEntryKind.EDIT)
    log_entry = qs_last(target_object.log_entries)
    log_entry.message = "sneak"
    with pytest.raises(ValueError):
        log_entry.save()


@pytest.mark.django_db
def test_user_logging(admin_user, target_object):
    target_object.add_log_entry(message="audit", kind=LogEntryKind.AUDIT, user=admin_user)
    log_entry = qs_last(target_object.log_entries)
    assert log_entry.user.is_superuser  # we put an admin in


@pytest.mark.django_db
def test_modify_before_save(target_object):
    le = target_object.add_log_entry(message="hi", save=False)
    le.message = "hey"
    le.save()
    le = qs_last(target_object.log_entries)
    assert le.message == "hey"


@pytest.mark.django_db
def test_custom_kind(target_object):
    le = target_object.add_log_entry(message="custom", kind="custom_kind")
    assert le.kind == 3010
    assert le.get_kind_display() == "very custom"


@pytest.mark.django_db
def test_invalid_kinds(target_object):
    with pytest.raises(UnknownLogKind):
        target_object.add_log_entry(message="custom", kind="is0wdfjgwr")

    with pytest.raises(UnknownLogKind):
        target_object.add_log_entry(message="custom", kind=43524)


@pytest.mark.django_db
def test_free_log_entries():
    fle = FreeLogEntry.add_log_entry(
        target=None,
        message="hello world"
    )
    assert fle.pk
    assert not fle.target
    assert qs_last(FreeLogEntry.objects.all()) == fle


@pytest.mark.django_db
def test_custom_kwarg():
    target_object = LoggedModel.objects.create()
    target_object.add_log_entry(message="shh", private=True)
    target_object.add_log_entry(message="yay", private=False)
    assert target_object.log_entries.filter(private=True).count() == 1
    assert target_object.log_entries.filter(private=False).count() == 1


@pytest.mark.django_db
def test_unsaved_object_logging_raises_error():
    target_object = LoggedModel()
    with pytest.raises(ValueError):
        target_object.add_log_entry(message="nope")
