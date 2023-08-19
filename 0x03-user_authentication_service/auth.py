#!/usr/bin/env python3
"""A module for authentication-related routines.
"""
from sqlalchemy.orm.exc import NoResultFound
from typing import Union

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

    def create_session(self, email: str) -> str:
        ''' Creates a new session id for a user.
        '''
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            return None
        if user:
            session_id = _generate_uuid()
            self._db.update_user(user.id, session_id=session_id)
            return session_id
        return None

    def get_user_from_session_id(self, session_id: str) -> Union[User, None]:
        ''' Retrieves a user based on a given session ID.
        '''
        if session_id is None:
            return None
        try:
            user = self._db.find_user_by(session_id=session_id)
        except NoResultFound:
            return None
        return user

    def destroy_session(self, user_id: int) -> None:
        ''' Destroys a session associated with a given user.
        '''
        if user_id is None:
            return None
        self._db.update_user(user_id, session_id=None)

    def get_reset_password_token(self, email: str) -> str:
        ''' Generates a password reset token for a user.
        '''
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            raise ValueError

        reset_token = _generate_uuid()
        self._db.update_user(user.id, reset_token=reset_token)
        return reset_token
