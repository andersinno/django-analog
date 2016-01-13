from analog.define import define_log_model
from django.db import models


class LoggedModel(models.Model):
    pass

LoggedModelLogEntry = define_log_model(LoggedModel)