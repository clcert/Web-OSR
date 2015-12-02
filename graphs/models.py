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


class ServiceMetadata(EmbeddedDocument):
    manufacturer = StringField()
    product = StringField()
    version = StringField()


class Metadata(EmbeddedDocument):
    device = EmbeddedDocumentField(DeviceMetadata)
    service = EmbeddedDocumentField(ServiceMetadata)


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
