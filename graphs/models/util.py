
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
        if ciphers is None:
            ciphers = {}

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


class SubjectIssuer(object):

    def __init__(self, subiss):
        if subiss is None:
            subiss = {}

        self.raw_information = subiss.get('raw_information')
        self.country_name = subiss.get('country_name')
        self.province_name = subiss.get('province_name')
        self.locality_name = subiss.get('locality_name')
        self.organization_name = subiss.get('organization_name')
        self.organization_unit_name = subiss.get('organization_unit_name')
        self.common_name = subiss.get('common_name')
        self.email_address = subiss.get('email_address')

    def to_json(self):
        return {
            'raw_information': self.raw_information,
            'country_name': self.country_name,
            'province_name': self.province_name,
            'locality_name': self.locality_name,
            'organization_name': self.organization_name,
            'organization_unit_name': self.organization_unit_name,
            'common_name': self.common_name,
            'email_address': self.email_address,
        }


class Certificate(object):

    def __init__(self, certificate):
        if certificate is None:
            certificate = {}

        self.subject = SubjectIssuer(certificate.get('subject'))
        self.issuer = SubjectIssuer(certificate.get('issuer'))
        self.not_before = certificate.get('not_before')
        self.not_after = certificate.get('not_after')
        self.key_bits = certificate.get('key_bits')
        self.signature_algorithm = certificate.get('signature_algorithm')
        self.pem_cert = certificate.get('pem_cert')

    def to_json(self):
        return {
            'subject': self.subject.to_json(),
            'issuer': self.issuer.to_json(),
            'not_before': self.not_before,
            'not_after': self.not_after,
            'key_bits': self.key_bits,
            'signature_algorithm': self.signature_algorithm,
            'pem_cert': self.pem_cert
        }


class HTTPS(object):

    def __init__(self, data):
        self.ip = data.get('ip')
        self.date = data.get('date')
        self.schema_version = data.get('schema_version')
        self.error = data.get('error')
        self.validate = data.get('validate')
        self.validation_error = data.get('validation_error')
        self.tls_protocol = data.get('tls_protocol')
        self.cipher_suite = data.get('cipher_suite')
        self.supported_protocols = TLSProtocols(data.get('supported_protocols'))
        self.supported_cipher_suites = CipherSuites(data.get('supported_cipher_suites'))
        self.beast_cipher = data.get('beast_cipher')
        self.heartbleed_data = data.get('heartbleed_data')
        self.chain = [Certificate(i) for i in data.get('chain')]

    def to_json(self):
        return {
            'ip': self.ip,
            'date': self.date,
            'schema_version': self.schema_version,
            'error': self.error,
            'validate': self.validate,
            'validation_error': self.validation_error,
            'tls_protocol': self.tls_protocol,
            'cipher_suite': self.cipher_suite,
            'supported_protocols': self.supported_protocols.to_json(),
            'supported_cipher_suites': self.supported_cipher_suites.to_json(),
            'beast_cipher': self.beast_cipher,
            'heartbleed_data': self.heartbleed_data,
            'chain': [cert.to_json() for cert in self.chain]
        }