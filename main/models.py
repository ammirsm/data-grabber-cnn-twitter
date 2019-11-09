from django.db import models
import json
from django.db import models
from django.utils import timezone


class Quote(models.Model):
    """
    The scrapped data will be saved in this model
    """
    text = models.TextField()
    author = models.CharField(max_length=512)


class News(models.Model):
    headline = models.CharField(max_length=5000)
    body = models.CharField(max_length=500000)
    url = models.CharField(max_length=5000)


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

