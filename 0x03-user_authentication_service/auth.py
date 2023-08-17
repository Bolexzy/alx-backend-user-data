#!/usr/bin/env python3
"""A module for authentication-related routines.
"""
from sqlalchemy.orm.exc import NoResultFound

import bcrypt
from user import User
from db import DB


def _hash_password(password: str) -> bytes:
    ''' Hash a password with bcrypt
    '''
    hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    return hashed


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        ''' Adds a new user to the database.
        '''
        try:
            self._db.find_user_by(email=email)
        except NoResultFound:
            return self._db.add_user(email, _hash_password(password))
        raise ValueError(f'User {email} already exists.')
