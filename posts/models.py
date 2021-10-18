from django.db import models
from core.models import TimeStampModel


class Post(TimeStampModel):
    post = models.TextField()
    author = models.ForeignKey("users.User", on_delete=models.CASCADE)
