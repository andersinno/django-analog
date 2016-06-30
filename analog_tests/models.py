from analog.define import define_log_model
from django.db import models

from analog.models import BaseLogEntry


class LoggedModel(models.Model):
    pass


LoggedModelLogEntry = define_log_model(LoggedModel)


class FreeLogEntry(BaseLogEntry):
    pass
