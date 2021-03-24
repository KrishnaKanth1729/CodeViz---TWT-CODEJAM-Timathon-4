import datetime
import random
import string
from .storage import OverwriteStorage
from django.db import models
from django.utils.timezone import now

def user_directory_path(instance, filename):
    return '{}'.format('file.py')


class PyFile(models.Model):
    file = models.FileField(storage=OverwriteStorage(), upload_to=user_directory_path)
    name = models.CharField(max_length=255)
    color = models.CharField(max_length=6, default='#fff000')

    def delete(self, *args, **kwargs):
        self.file.delete()
        super().delete(*args, **kwargs)

    def __str__(self):
        return self.name


class VizQuery(models.Model):
    text = models.TextField()

    def __str__(self):
        return self.text


class Candle(models.Model):
    ticker = models.CharField(max_length=255, default='AAPL')

    def __str__(self):
        return f'{self.ticker} '

