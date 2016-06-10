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
    success = models.BooleanField()
    data = JSONField()

    class Meta:
        db_table = 'http_port_80'
        ordering = ['ip']


class HTTP443(models.Model):
    ip = models.GenericIPAddressField(primary_key=True)
    date = models.DateField(primary_key=True)
    success = models.BooleanField()
    data = JSONField()

    class Meta:
        db_table = 'http_port_443'
        ordering = ['ip']


class HTTP8000(models.Model):
    ip = models.GenericIPAddressField(primary_key=True)
    date = models.DateField(primary_key=True)
    success = models.BooleanField()
    data = JSONField()

    class Meta:
        db_table = 'http_port_8000'
        ordering = ['ip']


class HTTP8080(models.Model):
    ip = models.GenericIPAddressField(primary_key=True)
    date = models.DateField(primary_key=True)
    success = models.BooleanField()
    data = JSONField()

    class Meta:
        db_table = 'http_port_8080'
        ordering = ['ip']


class HTTPServer(models.Model):
    port = models.IntegerField(primary_key=True)
    date = models.DateField(primary_key=True)
    product = models.TextField(primary_key=True)
    version = models.TextField(primary_key=True)
    total = models.IntegerField()

    class Meta:
        db_table = 'http_product'
        ordering = ['-total']


class HTTPOS(models.Model):
    port = models.IntegerField(primary_key=True)
    date = models.DateField(primary_key=True)
    os = models.TextField(primary_key=True)
    version = models.TextField(primary_key=True)
    total = models.IntegerField()

    class Meta:
        db_table = 'http_os'
        ordering = ['-total']


class HTTPType(models.Model):
    port = models.IntegerField(primary_key=True)
    date = models.DateField(primary_key=True)
    type = models.TextField(primary_key=True)
    total = models.IntegerField()

    class Meta:
        db_table = 'http_type'
        ordering = ['-total']


HTTP_PORT = {
    '80': HTTP80,
    '443': HTTP443,
    '8000': HTTP8000,
    '8080': HTTP8080
}
