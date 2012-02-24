from django.db import models

class QueueItem(models.Model):
    bugno    = models.IntegerField(primary_key=True)
    active   = models.BooleanField()
    reporter = models.CharField(max_length=80)
    owner    = models.CharField(max_length=80)
    subject  = models.CharField(max_length=160)
