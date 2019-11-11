from django.db import models
import json
from django.db import models
from django.utils import timezone

class News(models.Model):
    headline = models.CharField(max_length=5000)
    byline = models.CharField(max_length=10000)
    section = models.CharField(max_length=5000)
    byline = models.CharField(max_length=5000)
    picture = models.CharField(max_length=5000)
    body = models.CharField(max_length=500000)
    url = models.CharField(max_length=5000)
    created_at = models.DateTimeField(auto_now_add=True)


class ScrapyItem(models.Model):
    unique_id = models.CharField(max_length=100, null=True)
    data = models.TextField()  # this stands for our crawled data
    date = models.DateTimeField(default=timezone.now)

    # This is for basic and custom serialisation to return it to client as a JSON.
    @property
    def to_dict(self):
        data = {
            'data': json.loads(self.data),
            'date': self.date
        }
        return data

    def __str__(self):
        return self.unique_id


class Tweet(models.Model):
    tweet = models.CharField(max_length=500000)
    time = models.CharField(max_length=5000)
    link = models.CharField(max_length=5000)
    user = models.CharField(max_length=5000)
    user_picture = models.CharField(max_length=5000)
    user_name = models.CharField(max_length=5000)

    created_at = models.DateTimeField(auto_now_add=True)

