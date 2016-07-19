from django.db import models
from django.contrib.postgres.fields.array import ArrayField


class Asn(models.Model):
    number = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=1000)
    blocks = ArrayField(models.GenericIPAddressField())

    class Meta:
        db_table = 'asn'
        ordering = ['number']

    def __str__(self):
        return "Number = " + str(self.number) + ", Name = " + self.name + ", Bloques = " + str(self.blocks)

    def number_of_addresses(self):
        size = 0
        if self.blocks is None:
            return size
        for block in self.blocks:
            size += 2**(32 - int(block.split('/')[1]))
        return size


class AsnHTTPServer(models.Model):
    asn = models.IntegerField(primary_key=True)
    port = models.IntegerField(primary_key=True)
    date = models.DateField(primary_key=True)
    product = models.TextField(primary_key=True)
    version = models.TextField(primary_key=True)
    total = models.IntegerField()

    class Meta:
        db_table = 'http_product_asn'
        ordering = ['-total']


class AsnHTTPOS(models.Model):
    asn = models.IntegerField(primary_key=True)
    port = models.IntegerField(primary_key=True)
    date = models.DateField(primary_key=True)
    os = models.TextField(primary_key=True)
    version = models.TextField(primary_key=True)
    total = models.IntegerField()

    class Meta:
        db_table = 'http_os_asn'
        ordering = ['-total']


class AsnHTTPType(models.Model):
    asn = models.IntegerField(primary_key=True)
    port = models.IntegerField(primary_key=True)
    date = models.DateField(primary_key=True)
    type = models.TextField(primary_key=True)
    total = models.IntegerField()

    class Meta:
        db_table = 'http_type_asn_asn'
        ordering = ['-total']


class AsnHTTPSKeyBits(models.Model):
    asn = models.IntegerField(primary_key=True)
    port = models.IntegerField(primary_key=True)
    date = models.DateField(primary_key=True)
    valid = models.BooleanField(primary_key=True)
    bits = models.IntegerField(primary_key=True)
    total = models.IntegerField()

    class Meta:
        db_table = 'https_key_bits_asn'
        ordering = ['-total']


class AsnHTTPSSignature(models.Model):
    asn = models.IntegerField(primary_key=True)
    port = models.IntegerField(primary_key=True)
    date = models.DateField(primary_key=True)
    valid = models.BooleanField(primary_key=True)
    signature = models.TextField(primary_key=True)
    total = models.IntegerField()

    class Meta:
        db_table = 'https_signature_asn'
        ordering = ['-total']


class AsnHTTPSCipherSuite(models.Model):
    asn = models.IntegerField(primary_key=True)
    port = models.IntegerField(primary_key=True)
    date = models.DateField(primary_key=True)
    valid = models.BooleanField(primary_key=True)
    cipher_suite = models.TextField(primary_key=True)
    total = models.IntegerField()

    class Meta:
        db_table = 'https_cipher_suite_asn'
        ordering = ['-total']


class AsnHTTPSTlsProtocol(models.Model):
    asn = models.IntegerField(primary_key=True)
    port = models.IntegerField(primary_key=True)
    date = models.DateField(primary_key=True)
    valid = models.BooleanField(primary_key=True)
    protocol = models.TextField(primary_key=True)
    total = models.IntegerField()

    class Meta:
        db_table = 'https_tls_protocol_asn'
        ordering = ['-total']
