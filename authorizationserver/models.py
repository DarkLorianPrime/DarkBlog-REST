import datetime

from django.contrib.auth.models import AbstractUser
from django.db import models


class Roles(models.Model):
    role = models.CharField(max_length=255)


class User(AbstractUser):
    role = models.ManyToManyField(Roles)
    token = models.CharField(max_length=255)
    avatar = models.CharField(max_length=255, null=True, blank=True)


class PostToken(models.Model):
    expires = models.DateTimeField(default=datetime.datetime.now() + datetime.timedelta(minutes=30))
    token = models.CharField(max_length=255)