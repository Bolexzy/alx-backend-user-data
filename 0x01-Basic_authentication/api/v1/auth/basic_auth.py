#!/usr/bin/env python3
'''Basic authentication module for the API.
'''
import base64
from .auth import Auth


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
