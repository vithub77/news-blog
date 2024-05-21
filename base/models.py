from django.db import models
from django.contrib.auth.models import User


class NewsBd(models.Model):
    source = models.CharField(max_length=500)
    description = models.TextField(default='')
    url = models.CharField(max_length=500)
    data = models.DateTimeField(null=True)
    count_comments = models.IntegerField(default=0)

    def __str__(self):
        return self.url


class Comments(models.Model):
    news = models.ForeignKey(NewsBd, on_delete=models.CASCADE)
    author = models.CharField(max_length=100)
    text = models.TextField(default='')
    publication_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.author


class NewsBdEn(models.Model):
    source = models.CharField(max_length=500)
    description = models.TextField(default='')
    url = models.CharField(max_length=500)
    data = models.DateTimeField(null=True)
    count_comments = models.IntegerField(default=0)

    def __str__(self):
        return self.url


class CommentsEn(models.Model):
    news = models.ForeignKey(NewsBdEn, on_delete=models.CASCADE)
    author = models.CharField(max_length=100)
    text = models.TextField(default='')
    publication_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.author


class PosNews(models.Model):
    news = models.ForeignKey(NewsBd, on_delete=models.CASCADE)
    username = models.CharField(max_length=100, default='')


# class UserProfile(models.Model):
#     person = models.ForeignKey(User, on_delete=models.CASCADE, related_name='profile')
#     avatar = models.ImageField(upload_to='profile_photos', default='user.jpg')

    # @property
    # def avatar_url(self):
    #     if self.avatar and hasattr(self.avatar, 'url'):
    #         return self.avatar.url
