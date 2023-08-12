#!/usr/bin/env python3
'''Basic authentication module for the API.
'''
import base64
from .auth import Auth
import base64
from typing import Tuple, TypeVar

from models.user import User


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

    def extract_user_credentials(
            self,
            decoded_base64_authorization_header: str
            ) -> Tuple[str, str]:
        '''Extracts user credentials from a base64-decoded authorization header
        '''
        if isinstance(decoded_base64_authorization_header, str):
            if ':' in decoded_base64_authorization_header:
                return tuple(decoded_base64_authorization_header.split(':'))
        return (None, None)

    def user_object_from_credentials(
            self,
            user_email: str,
            user_pwd: str
            ) -> TypeVar('User'):
        ''' Retrieves a user based on the user's authentication credentials.
        '''
        if isinstance(user_email, str) and isinstance(user_pwd, str):
            try:
                users = User.search({'email': user_email})
            except Exception:
                return None
            if len(users) and users[0].is_valid_password(user_pwd):
                return users[0]

        return None
