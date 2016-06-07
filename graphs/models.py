from django.contrib.postgres.fields import JSONField
from django.db import models


class ZmapLog(models.Model):
    port = models.IntegerField(primary_key=True)
    date = models.DateField(primary_key=True)
    time = models.IntegerField()
    send = models.IntegerField()
    recv = models.IntegerField()
    hits = models.FloatField()

    class Meta:
        db_table = 'zmap_log'
        ordering = ['date']


class HTTP80(models.Model):
    ip = models.GenericIPAddressField(primary_key=True)
    date = models.DateField(primary_key=True)
    data = JSONField()

    class Meta:
        db_table = 'http_port_80'
        ordering = ['ip']

