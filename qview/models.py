from django.db import models

class QueueItem(models.Model):
    bugno    = models.IntegerField(primary_key=True)
    #
    active   = models.BooleanField()
    pending  = models.BooleanField()
    #
    reporter = models.CharField(max_length=80)
    owner    = models.CharField(max_length=80)
    subject  = models.CharField(max_length=160)
    msgid    = models.CharField(max_length=256)
    severity = models.CharField(max_length=80)
    # scraped info
    package  = models.CharField(max_length=80)
    descr    = models.CharField(max_length=80)
    version  = models.CharField(max_length=80)

    def get_tags(self):
        tags = Tag.objects.filter(
            bugno=self.bugno
        )
        return tags

class Tag(models.Model):
    name     = models.CharField(max_length=80)
    bugno    = models.IntegerField()
