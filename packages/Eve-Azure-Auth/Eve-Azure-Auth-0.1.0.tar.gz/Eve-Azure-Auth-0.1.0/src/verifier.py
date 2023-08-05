import jwt
import requests
from cachecontrol import CacheControl

from .jwksutils import rsa_pem_from_jwk


class InvalidAuthorizationToken(Exception):
    def __init__(self, details):
        super().__init__('Invalid authorization token: ' + details)


class AzureVerifier:
    api_version = 'v2.0'
    authority = 'https://login.microsoftonline.com'
    tenant = 'common'
    discovery_document = '.well-known/openid-configuration'

    audiences = None
    issuer = None

    def __init__(self, tenant='common', issuer=None, audiences=None):
        self.tenant = tenant or self.tenant
        self.issuer = issuer
        self.audiences = audiences
        self.session = CacheControl(requests.Session())

    @property
    def documents_uri(self):
        return f'{self.authority}/{self.tenant}/{self.api_version}/{self.discovery_document}'

    @property
    def jwks_uri(self):
        return self.session.get(self.documents_uri).json()['jwks_uri']

    @property
    def jwks(self):
        return self.session.get(self.jwks_uri).json()

    def get_jwk(self, kid):
        for jwk in self.jwks.get('keys'):
            if jwk.get('kid') == kid:
                return jwk
        raise InvalidAuthorizationToken('kid not recognized')

    def get_kid(self, token):
        headers = jwt.get_unverified_header(token)
        if not headers:
            raise InvalidAuthorizationToken('missing headers')
        try:
            return headers['kid']
        except KeyError:
            raise InvalidAuthorizationToken('missing kid')

    def get_public_key(self, token):
        return rsa_pem_from_jwk(self.get_jwk(self.get_kid(token)))

    def verify(self, token):
        public_key = self.get_public_key(token)

        return jwt.decode(
            token, public_key, verify=True, algorithms=['RS256'], audience=self.audiences, issuer=self.issuer
        )
