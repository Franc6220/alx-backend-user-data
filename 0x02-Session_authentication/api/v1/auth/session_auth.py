#!/usr/bin/env python3
""" SessionAuth module
"""
import os
from api.v1.auth.auth import Auth
import uuid
from models.user import User

class SessionAuth(Auth):
    """ SessionAuth class that inherits from Auth
    """

    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """ Create a session ID for a user_id
        """
        if user_id is None or not isinstance(user_id, str):
            return None

        session_id = str(uuid.uuid4())
        self.user_id_by_session_id[session_id] = user_id
        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """ Return a User ID based on a Session ID
        """
        if session_id is None or not isinstance(session_id, str):
            return None

        return self.user_id_by_session_id.get(session_id)

    def session_cookie(self, request=None):
        """Returns the session cookie from the request"""
        if request is None:
            return None
        session_name = os.getenv("SESSION_NAME")
        return request.cookies.get(session_name)

    def current_user(self, request=None):
        """Returns the current User instance based on the session cookie"""
        if request is None:
            return None

        # Get the session ID from the cookie
        session_id = self.session_cookie(request)
        if session_id is None:
            return None

        # Get the user ID based on the session ID
        user_id = self.user_id_for_session_id(session_id)
        if user_id is None:
            return None

        # Retrieve and return the User instance based on the user ID
        return User.get(user_id)

    def destroy_session(self, request=None):
        """Deletes the user session (logout)"""
        if request is None:
            return False

        session_id = self.session_cookie(request)
        if session_id is None:
            return False

        user_id = self.user_id_for_session_id(session_id)
        if user_id is None:
            return False

        if session_id in self.user_id_by_session_id:
            del self.user_id_by_session_id[session_id]
            return True

        return False
