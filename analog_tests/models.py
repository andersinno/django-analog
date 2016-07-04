from analog.define import define_log_model
from django.db import models

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
