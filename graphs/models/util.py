
class DeviceMetadata(object):

    def __init__(self, device):
        if device is None:
            device = {}

        self.manufacturer = device.get('manufacturer')
        self.product = device.get('product')
        self.os = device.get('os')
        self.os_version = device.get('os_version')
        self.type = device.get('type')

    def to_json(self):
        return {
            'manufacturer': self.manufacturer,
            'product': self.product,
            'os': self.os,
            'os_device': self.os_version,
            'type': self.type
        }


class ServiceMetadata(object):

    def __init__(self, service):
        if service is None:
            service = {}

        self.manufacturer = service.get('manufacturer')
        self.product = service.get('product')
        self.version = service.get('version')

    def to_json(self):
        return {
            'manufacturer': self.manufacturer,
            'product': self.product,
            'version': self.version
        }


class Metadata(object):

    def __init__(self, metadata):
        if metadata is None:
            metadata = {}

        self.device = DeviceMetadata(metadata.get('device'))
        self.service = ServiceMetadata(metadata.get('service'))

    def to_json(self):
        return {
            'device': self.device.to_json(),
            'service': self.service.to_json()
        }


class HTTP(object):

    def __init__(self, data):
        self.ip = data.get('ip')
        self.date = data.get('date')
        self.schema_version = data.get('schema_version')
        self.error = data.get('error')
        self.status = data.get('status')
        self.raw_header = data.get('raw_header')
        self.parse_header = data.get('parse_header')
        self.raw_index = data.get('raw_index')
        self.parse_index = data.get('parse_index')
        self.metadata = Metadata(data.get('metadata'))

    def to_json(self):
        return {
            'ip': self.ip,
            'date': self.date,
            'schema_version': self.schema_version,
            'error': self.error,
            'status': self.status,
            'raw_header': self.raw_header,
            'parse_header': self.parse_header,
            'raw_index': self.raw_index,
            'parse_index': self.parse_index,
            'metadata': self.metadata.to_json()
        }


class TLSProtocols(object):

    def __init__(self, protocols):
        if protocols is None:
            protocols = {}

        self.TLS_12 = protocols.get('TLS_12')
        self.TLS_11 = protocols.get('TLS_11')
        self.TLS_10 = protocols.get('TLS_10')
        self.SSL_30 = protocols.get('SSL_30')

    def to_json(self):
        return {
            'TLS_12': self.TLS_12,
            'TLS_11': self.TLS_11,
            'TLS_10': self.TLS_10,
            'SSL_30': self.SSL_30
        }


class CipherSuites(object):

    def __init__(self, ciphers):
        self.null_ciphers = ciphers.get('null_ciphers')
        self.anonymous_null_ciphers = ciphers.get('anonymous_null_ciphers')
        self.anonymous_dh_ciphers = ciphers.get('anonymous_dh_ciphers')
        self.export_40_ciphers = ciphers.get('export_40_ciphers')
        self.low_ciphers = ciphers.get('low_ciphers')
        self.medium_ciphers = ciphers.get('medium_ciphers')
        self.des3_ciphers = ciphers.get('des3_ciphers')
        self.high_ciphers = ciphers.get('high_ciphers')
        self.freak = ciphers.get('freak')
        self.logjam = ciphers.get('logjam')

    def to_json(self):
        return {
            'null_ciphers': self.null_ciphers,
            'anonymous_null_ciphers': self.anonymous_null_ciphers,
            'anonymous_dh_ciphers': self.anonymous_dh_ciphers,
            'export_40_ciphers': self.export_40_ciphers,
            'low_ciphers': self.low_ciphers,
            'medium_ciphers': self.medium_ciphers,
            'des3_ciphers': self.des3_ciphers,
            'high_ciphers': self.high_ciphers,
            'freak': self.freak,
            'logjam': self.logjam
        }

# class Certificate(object):
#
#     def __init__(self, data):