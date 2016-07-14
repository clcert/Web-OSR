from django.db import models
from django.contrib.postgres.fields.array import ArrayField


class Asn(models.Model):
    number = models.IntegerField(primary_key=True)
    name = models.CharField()
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
