from django.db import models

from analog.define import define_log_model
from analog.models import BaseLogEntry


class LoggedModel(models.Model):
    pass


class PrivateLogEntry(BaseLogEntry):
    private = models.BooleanField(default=False, db_index=True)

    class Meta:
        abstract = True


LoggedModelLogEntry = define_log_model(LoggedModel, base_class=PrivateLogEntry)


class FreeLogEntry(BaseLogEntry):
    pass


class SecondLoggedModel(models.Model):
    pass


SecondLoggedModelLogEntry = define_log_model(
    SecondLoggedModel, allow_null_target=True)


class ExtraLogEntry(BaseLogEntry):
    extra = models.CharField(null=True, blank=True, max_length=64)


class ThirdLoggedModel(models.Model):
    pass


ThirdLoggedModelLogEntry = define_log_model(
    ThirdLoggedModel, base_class=ExtraLogEntry)
