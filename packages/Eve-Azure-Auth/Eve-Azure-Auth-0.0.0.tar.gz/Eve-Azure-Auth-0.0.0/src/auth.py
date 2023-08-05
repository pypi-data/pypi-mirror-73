from eve.auth import TokenAuth
from flask import current_app as app

from .verifier import AzureVerifier


class AzureAuth(TokenAuth):

    def validate_token(self, token):
        tenant = app.configget('AZURE_AD_TENANT')
        issuer = app.config['AZURE_AD_ISSUER']
        audiences = app.config['AZURE_AD_AUDIENCES']

        try:
            return AzureVerifier(tenant, issuer, audiences).verify(token)
        except Exception as e:
            app.logger.error(e)
        return False

    def check_auth(self, token, allowed_roles, resource, method):
        return self.validate_token(token)
