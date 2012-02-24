from django.db import models

class QueueItem(models.Model):
    active   = models.BooleanField()
    reporter = models.CharField(max_length=80)
    owner    = models.CharField(max_length=80)
    subject  = models.CharField(max_length=160)
