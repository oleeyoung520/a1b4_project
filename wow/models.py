from django.db import models
import datetime


class Input(models.Model):
    objects = models.Manager()
    
    title = models.CharField(max_length=50)
    date = models.DateField(default=datetime.date.today)
    members = models.CharField(max_length=60)
    tag = models.CharField(max_length=10)
    wav = models.FileField(upload_to="")

