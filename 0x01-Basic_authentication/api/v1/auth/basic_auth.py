#!/usr/bin/env python3
'''Basic authentication module for the API.
'''
import base64
from .auth import Auth
import base64


class BasicAuth(Auth):
    ''' Represents Basic authentication.
    '''

    def extract_base64_authorization_header(
            self,
            authorization_header: str
            ) -> str:
        ''' Extracts the Base64 part of the Authorization header
        for a Basic Authentication.
        '''
        if isinstance(authorization_header, str):
            if authorization_header.startswith("Basic "):
                return authorization_header[6:]
        else:
            return None

    def decode_base64_authorization_header(
            self,
            base64_authorization_header: str
            ) -> str:
        ''' Decodes a base64-encoded authorization header.
        '''
        if isinstance(base64_authorization_header, str):
            try:
                result = base64.b64decode(
                        base64_authorization_header,
                        validate=True,
                        )
                return result.decode('utf-8')
            except (base64.binascii.Error, UnicodeDecodeError):
                return None
