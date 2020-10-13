import pytest
from django.db import models

from analog import BaseLogEntry, LogEntryKind, define_log_model
from analog.exceptions import NoExtraField, UnknownLogKind
from analog_tests.models import (
    FreeLogEntry, LoggedModel, LoggedModelLogEntry, SecondLoggedModel,
    ThirdLoggedModel)


class RandomModel(models.Model):
    pass


@pytest.fixture(params=["free", "target"])
@pytest.mark.django_db
def target_object(request):
    return create_target_object(request.param)


def create_target_object(kind):
    assert kind in ("free", "target")
    if kind == "target":
        return LoggedModel.objects.create()
    else:
        class FakeModel:
            pk = None

            def add_log_entry(self, **kwargs):
                return FreeLogEntry.add_log_entry(target=None, **kwargs)

            log_entries = FreeLogEntry.objects.all()

        return FakeModel()


def test_model_sanity():
    log_entry_model = define_log_model(RandomModel)
    assert log_entry_model.__module__ == RandomModel.__module__
    target_field = log_entry_model._meta.get_field("target")
    assert target_field.related_model is RandomModel
    try:
        rel = RandomModel.log_entries.related
        # TODO: Assert here too?
    except AttributeError:  # Django 1.9+
        rel = RandomModel.log_entries.rel
        assert rel.model is RandomModel
        assert rel.related_model is log_entry_model

    assert issubclass(log_entry_model, BaseLogEntry)
    assert isinstance(log_entry_model(), BaseLogEntry)


@pytest.mark.django_db
@pytest.mark.parametrize("target_type,arg_type", [
    ("free", "kwargs"),
    ("target", "args"),
    ("target", "kwargs"),
    # Note: ("free", "args") is ommitted here, because free log entries
    # do not support kwargless api
])
def test_add_log_entry(target_type, arg_type):
    target_object = create_target_object(target_type)
    if target_object.pk:
        # yigh, for some reason I don't care to look into more deeply (you
        # know what they say about abysses), Django 1.4 sometimes hasn't
        # actually saved this object correctly. So save it again just in case.
        target_object.save()

    if arg_type == "kwargs":
        target_object.add_log_entry(message="hello, world")
    else:
        assert target_object.pk
        target_object.add_log_entry("hello, world")
    assert target_object.log_entries.count() == 1
    log_entry = target_object.log_entries.last()
    if log_entry.target:
        assert isinstance(log_entry, LoggedModelLogEntry)
    assert isinstance(log_entry, BaseLogEntry)


@pytest.mark.django_db
def test_log_entry_kind(target_object):
    target_object.add_log_entry(message="edited", kind=LogEntryKind.EDIT)
    log_entry = target_object.log_entries.last()
    assert log_entry.get_kind_display() == "edit"


@pytest.mark.django_db
def test_log_mutation(target_object):
    target_object.add_log_entry(
        message="benign action",
        kind=LogEntryKind.EDIT)
    log_entry = target_object.log_entries.last()
    log_entry.message = "sneak"
    with pytest.raises(ValueError):
        log_entry.save()


@pytest.mark.django_db
def test_user_logging(admin_user, target_object):
    target_object.add_log_entry(
        message="audit",
        kind=LogEntryKind.AUDIT,
        user=admin_user)
    log_entry = target_object.log_entries.last()
    assert log_entry.user.is_superuser  # we put an admin in


@pytest.mark.django_db
def test_modify_before_save(target_object):
    le = target_object.add_log_entry(message="hi", save=False)
    le.message = "hey"
    le.save()
    le = target_object.log_entries.last()
    assert le.message == "hey"


@pytest.mark.django_db
def test_extra_with_no_extra_field_is_an_error(target_object):
    with pytest.raises(NoExtraField):
        target_object.add_log_entry(message="hi", extra={'henlo': 'fren'})


@pytest.mark.django_db
def test_extra_field():
    target_object = ThirdLoggedModel.objects.create()
    target_object.add_log_entry(message="hi", extra='hoi')
    assert target_object.log_entries.last().extra == 'hoi'


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
    assert FreeLogEntry.objects.last() == fle


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


@pytest.mark.django_db
def test_nullable_log_model():
    m = SecondLoggedModel.objects.create()
    m.add_log_entry(message="hello")
    log_entry_model = SecondLoggedModel.log_model
    log_entry_model.objects.create(message="world")
    assert log_entry_model.objects.first().target == m
    assert log_entry_model.objects.last().target is None
