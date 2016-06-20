
class DeviceMetadata(object):

    def __init__(self, device):
        if device is None:
            device = {}

        self.manufacturer = device.get('manufacturer')
        self.product = device.get('device')
        self.os = device.get('os')
        self.os_version = device.get('os_version')
        self.type = device.get('type')


class ServiceMetadata(object):

    def __init__(self, service):
        if service is None:
            service = {}

        self.manufacturer = service.get('manufacturer')
        self.product = service.get('device')
        self.version = service.get('version')


class Metadata(object):

    def __init__(self, metadata):
        if metadata is None:
            metadata = {}

        self.device = DeviceMetadata(metadata.get('device'))
        self.service = ServiceMetadata(metadata.get('service'))


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

