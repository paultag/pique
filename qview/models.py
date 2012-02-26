from django.db import models

class QueueItem(models.Model):
    SEVERITIES = (
        (u'C', u'critical'),
        (u'G', u'grave'),
        (u'S', u'serious'),
        (u'I', u'important'),
        (u'N', u'normal'),
        (u'M', u'minor'),
        (u'W', u'wishlist'),
    )
    bugno    = models.IntegerField(primary_key=True)
    #
    active   = models.BooleanField()
    pending  = models.BooleanField()
    #
    reporter = models.CharField(max_length=80)
    owner    = models.CharField(max_length=80)
    subject  = models.CharField(max_length=160)
    msgid    = models.CharField(max_length=256)
    severity = models.CharField(max_length=2, choices=SEVERITIES)
    # scraped info
    package  = models.CharField(max_length=80)
    descr    = models.CharField(max_length=80)
    version  = models.CharField(max_length=80)
    # XXX: ToDo: Tags
