from django.contrib.postgres.fields import JSONField
from django.db import models


class Certificate(models.Model):
    ip = models.GenericIPAddressField(primary_key=True)
    date = models.DateField(primary_key=True)
    success = models.BooleanField()
    data = JSONField()

    class Meta:
        db_table = 'https_port_443'
        ordering = ['ip']


class HTTPSKeyBits(models.Model):
    port = models.IntegerField(primary_key=True)
    date = models.DateField(primary_key=True)
    valid = models.BooleanField(primary_key=True)
    bits = models.IntegerField(primary_key=True)
    total = models.IntegerField()

    class Meta:
        db_table = 'https_key_bits'
        ordering = ['-total']