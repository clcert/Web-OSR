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


class HTTPSSignature(models.Model):
    port = models.IntegerField(primary_key=True)
    date = models.DateField(primary_key=True)
    valid = models.BooleanField(primary_key=True)
    signature = models.TextField(primary_key=True)
    total = models.IntegerField()

    class Meta:
        db_table = 'https_signature'
        ordering = ['-total']


class HTTPSCipherSuite(models.Model):
    port = models.IntegerField(primary_key=True)
    date = models.DateField(primary_key=True)
    valid = models.BooleanField(primary_key=True)
    cipher_suite = models.TextField(primary_key=True)
    total = models.IntegerField()

    class Meta:
        db_table = 'https_cipher_suite'
        ordering = ['-total']


class HTTPSTlsProtocol(models.Model):
    port = models.IntegerField(primary_key=True)
    date = models.DateField(primary_key=True)
    valid = models.BooleanField(primary_key=True)
    protocol = models.TextField(primary_key=True)
    total = models.IntegerField()

    class Meta:
        db_table = 'https_tls_protocol'
        ordering = ['-total']
