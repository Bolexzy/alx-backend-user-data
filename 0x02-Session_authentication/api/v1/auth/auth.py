#!/usr/bin/env python3
''' Defines an Auth class module
for our authentication system
'''

from flask import request
from typing import List, TypeVar
import os


class Auth():
    ''' Authentication class system.
    '''
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        ''' Check if path requires authentication
        Return true if path is not in the list, otherwise False.
        '''
        if path is not None and excluded_paths:
            if not path.endswith('/'):
                path += '/'
            for excluded_path in excluded_paths:
                if excluded_path.endswith("*") \
                        and path.startswith(excluded_path[:-1]):
                    return False
                elif path == excluded_path:
                    return False
        return True

    def authorization_header(self, request=None) -> str:
        ''' Return None
        '''
        # Get the value of the "Authorization" header
        auth_header = request.headers.get('Authorization')

        if request is None or auth_header is None:
            return None
        else:
            return auth_header

    def current_user(self, request=None) -> TypeVar('User'):
        ''' Return None
        '''
        return None

    def session_cookie(self, request=None):
        ''' Gets the value of the cookie named SESSION_NAME.
        '''
        if request:
            cookie_name = os.getenv('SESSION_NAME')
            return request.cookies.get(cookie_name)
