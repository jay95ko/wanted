from django.db import models
from core.models import TimeStampModel


class User(TimeStampModel):
    email = models.CharField(max_length=100)
    name = models.CharField(max_length=40)
    password = models.CharField(max_length=200)
