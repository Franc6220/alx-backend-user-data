#!/usr/bin/env python3
"""
Module for handling session expiration in session authentication.
Provides functionality to create and manage sessions with expiration.
"""

from os import getenv
from datetime import datetime, timedelta
from api.v1.auth.session_auth import SessionAuth

class SessionExpAuth(SessionAuth):
    """
    SessionExpAuth class that adds expiration to session IDs.

    Attributes:
        session_duration (int): Duration of the session in seconds.
    """

    def __init__(self):
        """Initialize session duration from environment variable."""
        super().__init__()
        try:
            self.session_duration = int(getenv('SESSION_DURATION', 0))
        except ValueError:
            self.session_duration = 0

    def create_session(self, user_id=None):
        """
        Create a session ID for a user with an expiration timestamp.

        Args:
            user_id (str): The ID of the user to create a session for.

        Returns:
            str: The created session ID or None if failed.
        """
        session_id = super().create_session(user_id)
        if not session_id:
            return None

        session_dict = {
                "user_id": user_id,
                "created_at": datetime.now()
        }
        self.user_id_by_session_id[session_id] = session_data
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """
        Return the user ID for a session if it is not expired.

        Args:
            session_id (str): The session ID to check.

        Returns:
            str: The user ID if session is valid, None otherwise.
        """
        if session_id is None:
            return None

        session_data = self.user_id_by_session_id.get(session_id)
        if session_data is None:
            return None

        user_id = session_data.get('user_id')
        created_at = session_data.get('created_at')

        if self.session_duration <= 0:
            return user_id

        if created_at is None:
            return None

        if created_at + timedelta(seconds=self.session_duration) < datetime.now():
            return None

        return user_id
