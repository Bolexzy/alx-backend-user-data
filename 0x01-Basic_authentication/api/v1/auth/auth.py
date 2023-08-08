#!/usr/bin/env python3
''' Defines an Auth class module
for our authentication system
'''

from flask import request
from typing import List, TypeVar


class Auth():
    ''' Authentication class system.
    '''
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        ''' Check if path requires authentication
        Return true if path is not in the list, otherwise False.
        '''
        if path is not None and not(
                excluded_paths is None or excluded_paths == []):
            if not path.endswith('/'):
                path += '/'
            if path in excluded_paths:
                return False
        return True

    def authorization_header(self, request=None) -> str:
        ''' Return None
        '''
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        ''' Return None
        '''
        return None
