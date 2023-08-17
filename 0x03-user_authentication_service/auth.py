#!/usr/bin/env python3
"""A module for authentication-related routines.
"""
from sqlalchemy.orm.exc import NoResultFound

import bcrypt
from user import User
from db import DB
from uuid import uuid4


def _hash_password(password: str) -> bytes:
    ''' Hash a password with bcrypt
    '''
    hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    return hashed


def _generate_uuid() -> str:
    """ Generates a UUID.
    """
    return str(uuid4())


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
        raise ValueError('User {} already exists.'.format(email))

    def valid_login(self, email: str, password: str) -> bool:
        ''' Checks if a user's login details are valid.
        '''
        try:
            user = self._db.find_user_by(email=email)
            if user:
                return bcrypt.checkpw(
                        password.encode('utf-8'),
                        user.hashed_password,
                        )
        except NoResultFound:
            return False
        return False
