from django.db import models


class Post(models.Model):
    author = models.ForeignKey('authorizationserver.User', on_delete=models.CASCADE, related_name='user_post')
    title = models.CharField(max_length=100)
    text = models.TextField(max_length=2000)
    is_published = models.BooleanField()
    created_at = models.DateTimeField(null=True, blank=True)
    blog = models.ForeignKey('blogs.Blog', on_delete=models.CASCADE, related_name='blog_post')
    views = models.ManyToManyField('authorizationserver.User', related_name='views_posts', blank=True)
    likes = models.ManyToManyField('authorizationserver.User', related_name='likes_posts', blank=True)


class Comment(models.Model):
    author = models.ForeignKey('authorizationserver.User', on_delete=models.CASCADE, related_name='comment_user')
    text = models.TextField(max_length=200)
    post = models.ForeignKey('Post', on_delete=models.CASCADE, related_name='comment_post')
    like = models.ManyToManyField('authorizationserver.User', related_name='comments_likes', blank=True)