from django.db import models
from mongoengine import connect, Document, StringField, DictField, ListField, EmbeddedDocument, EmbeddedDocumentField
from web.settings import MONGODB

connect(MONGODB['NAME'], host=MONGODB['HOST'], port=MONGODB['PORT'])


class DeviceMetadata(EmbeddedDocument):
    manufacturer = StringField()
    product = StringField()
    os = StringField()
    os_version = StringField()
    type = StringField()

    def __str__(self):
        return str({
            'manufacturer': self.manufacturer,
            'product': self.product,
            'os': self.os,
            'os_version': self.os_version,
            'type': self.type
        })


class ServiceMetadata(EmbeddedDocument):
    manufacturer = StringField()
    product = StringField()
    version = StringField()

    def __str__(self):
        return str({
            'manufacturer': self.manufacturer,
            'product': self.product,
            'version': self.version
        })


class Metadata(EmbeddedDocument):
    device = EmbeddedDocumentField(DeviceMetadata)
    service = EmbeddedDocumentField(ServiceMetadata)

    def __str__(self):
        return str({
            'device': self.device.__str__(),
            'service': self.service.__str__()
        })


class Http(Document):
    ip = StringField()
    date = StringField()
    error = StringField()
    response = StringField()
    server = StringField()
    content_type = StringField()
    www_authenticate = StringField()
    header = ListField()
    index = StringField()
    whois = DictField()
    dns_reverse = StringField()
    metadata = EmbeddedDocumentField(Metadata)

    meta = {
        'collection': 'port-80',
        'strict': False,
    }

    def __str__(self):
        return str({
            'ip': self.ip,
            'metadata': self.metadata.__str__()
        })


class Http80(Document):
    ip = StringField()
    date = StringField()
    error = StringField()
    response = StringField()
    server = StringField()
    content_type = StringField()
    www_authenticate = StringField()
    header = ListField()
    index = StringField()
    whois = DictField()
    dns_reverse = StringField()
    metadata = EmbeddedDocumentField(Metadata)

    meta = {
        'collection': 'port-80',
        'strict': False,
    }

    def __str__(self):
        return str({
            'ip': self.ip,
            'metadata': self.metadata.__str__()
        })


class Http8000(Document):
    ip = StringField()
    date = StringField()
    error = StringField()
    response = StringField()
    server = StringField()
    content_type = StringField()
    www_authenticate = StringField()
    header = ListField()
    index = StringField()
    whois = DictField()
    dns_reverse = StringField()
    metadata = EmbeddedDocumentField(Metadata)

    meta = {
        'collection': 'port-8000',
        'strict': False,
    }

    def __str__(self):
        return str({
            'ip': self.ip,
            'metadata': self.metadata.__str__()
        })
