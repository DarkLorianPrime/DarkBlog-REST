from django.contrib.auth.models import AbstractUser
from django.db import models


class Roles(models.Model):
    role = models.CharField(max_length=255)


class User(AbstractUser):
    role = models.ManyToManyField('Roles')
    # sub_blog = models.ManyToManyField('blogs.Blog') To-Do - Подписки на блоги
    description = models.TextField()
    avatar = models.CharField(max_length=255, null=True, blank=True)  # temporarily removed (Мне лень делать это)
