from django.db import models


class NewsBd(models.Model):
    source = models.CharField(max_length=500)
    description = models.TextField(default='')
    url = models.CharField(max_length=500)
    data = models.DateTimeField(null=True)

    def __str__(self):
        return self.source, self.description


class Comments(models.Model):
    news = models.ForeignKey(NewsBd, on_delete=models.CASCADE)
    author = models.CharField(max_length=100)
    text = models.TextField(default='')
    publication_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.author, self.text
