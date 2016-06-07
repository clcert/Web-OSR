from django.contrib.postgres.fields import JSONField
from django.db import models


class ZmapLog(models.Model):
    port = models.IntegerField()
    date = models.DateField()
    time = models.IntegerField()
    send = models.IntegerField()
    recv = models.IntegerField()
    hits = models.FloatField()

    class Meta:
        db_table = 'zmap_log'
        ordering = 'date'


class HTTP80(models.Model):
    ip = models.IPAddressField()
    date = models.DateField()
    data = JSONField()

    class Meta:
        db_table = 'http_port_80'
        ordering = 'ip'

