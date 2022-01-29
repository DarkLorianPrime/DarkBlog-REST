from django.db import models


class Blog(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(max_length=500, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey('authorizationserver.User', on_delete=models.CASCADE, related_name='blog_user')
    authors = models.ManyToManyField('authorizationserver.User', related_name='authors_users', blank=True)


