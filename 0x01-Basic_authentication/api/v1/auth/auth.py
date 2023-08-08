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
        ''' Check if path is in the list of excluded_paths
        Return true if path is not in the list, otherwise False.
        '''
        if path is not None and not path.endswith('/'):
            path += '/'

        if path is None or path not in excluded_paths\
                or excluded_paths is None or excluded_paths == []:
            return True
        return False

    def authorization_header(self, request=None) -> str:
        ''' Return None
        '''
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        ''' Return None
        '''
        return None
