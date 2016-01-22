from django.db import models

from mongoengine import connect, Document, StringField, DictField, ListField, EmbeddedDocument, EmbeddedDocumentField, \
    DateTimeField, IntField, BooleanField
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
        'abstract': True
    }

    def __str__(self):
        return str({
            'ip': self.ip,
            'date': self.date,
            'metadata': self.metadata.__str__()
        })


class Http80(Http):
    meta = {
        'collection': 'port-80',
        'strict': False,
        'ordering': ['date'],
        'indexes': ['#date']
    }


class Http443(Http):
    meta = {
        'collection': 'port-443',
        'strict': False,
        'ordering': ['date'],
        'indexes': ['#date']

    }


class Http8000(Http):
    meta = {
        'collection': 'port-8000',
        'strict': False,
        'ordering': ['date'],
        'indexes': ['#date']
    }


class Http8080(Http):
    meta = {
        'collection': 'port-8080',
        'strict': False,
        'ordering': ['date'],
        'indexes': ['#date']
    }


class ZmapLog(Document):
    port = StringField()
    date = DateTimeField()
    time = StringField()
    send = StringField()
    send_avg = StringField()
    recv = StringField()
    recv_avg = StringField()
    hits = StringField

    meta = {
        'collection': 'zmap_logs',
        'strict': False,
        'ordering': ['date']
    }


class GrabberScan(Document):
    port = StringField()
    date = DateTimeField()
    protocol = StringField()
    amount = StringField()

    meta = {
        'collection': 'grabber_scan',
        'ordering': ['date']
    }


# Todo complete the model
class Https(Document):
    ip = StringField()
    date = StringField()
    error = StringField()
    tls_protocol = StringField()
    cipher_suite = StringField()
    certificate_authority = StringField()
    signature_algorithm = StringField()
    key_bits = IntField()
    chain = ListField()
    valid = BooleanField(db_field='validate')

    meta = {
        'collection': 'port_443_cert',
        'strict': False
    }


class HttpWebServer(Document):
    port = StringField()
    scan = StringField()
    product = StringField()
    version = StringField()
    count = IntField()

    meta = {
           'collection': 'http_web_server',
           'strict': False
    }


class HttpOperativeSystem(Document):
    port = StringField()
    scan = StringField()
    operative_system = StringField()
    version = StringField()
    count = IntField()

    meta = {
           'collection': 'http_operative_system',
           'strict': False
    }


class HttpDeviceType(Document):
    port = StringField()
    scan = StringField()
    device_type = StringField()
    count = IntField()

    meta = {
           'collection': 'http_device_type',
           'strict': False
    }


