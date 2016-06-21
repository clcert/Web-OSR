
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

