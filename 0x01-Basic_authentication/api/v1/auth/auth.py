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
        ''' Returm false
        '''
        return False

    def authorization_header(self, request=None) -> str:
        ''' Return None
        '''
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        ''' Return None
        '''
        return None
