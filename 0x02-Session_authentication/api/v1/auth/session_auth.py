#!/usr/bin/env python3
"""Session authentication module for the API.
"""
from uuid import uuid4

from .auth import Auth
from models.user import User


class SessionAuth(Auth):
    ''' Session authentication class.
    '''

    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        ''' Creates a session id for the user.
        '''
        if isinstance(user_id, str):
            session_id = str(uuid4())
            self.user_id_by_session_id[session_id] = user_id
            return session_id

    def user_id_for_session_id(
            self, session_id: str = None
            ) -> str:
        ''' Retrieves the user id of the user associated with
        a given session id.
        '''
        if isinstance(session_id, str):
            return self.user_id_by_session_id.get(session_id)

    def current_user(self, request=None):
        ''' Retrieves the user associated with the request.
        '''
        user_id = self.user_id_for_session_id(
                self.session_cookie(request)
                )
        return User.get(user_id)
