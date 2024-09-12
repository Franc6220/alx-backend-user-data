#!/usr/bin/env python3
""" SessionDBAuth module """

import json
from datetime import datetime, timedelta
from os import getenv
from typing import Dict, Type
from api.v1.auth.session_exp_auth import SessionExpAuth
from models.user_session import UserSession

class SessionDBAuth(SessionExpAuth):
    """ SessionDBAuth class to handle session with database """

    def __init__(self):
        """ Initialize SessionDBAuth """
        super().__init__()
        self.user_sessions_file = 'user_sessions.json'
        self.load_user_sessions()

    def load_user_sessions(self):
        """ Load user sessions from the file """
        try:
            with open(self.user_sessions_file, 'r') as f:
                self.user_id_by_session_id = json.load(f)
        except FileNotFoundError:
            self.user_id_by_session_id = {}

    def save_user_sessions(self):
        """ Save user sessions to the file """
        with open(self.user_sessions_file, 'w') as f:
            json.dump(self.user_id_by_session_id, f)

    def create_session(self, user_id=None):
        """ Create a session and store in database """
        session_id = super().create_session(user_id)
        if session_id is None:
            return None

        session_dict = {
                'user_id': user_id,
                'created_at': datetime.now().isoformat()
                }
        self.user_id_by_session_id[session_id] = session_dict
        self.save_user_sessions()
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """ Get user ID from session ID """
        if session_id is None:
            return None

        session_dict = self.user_id_by_session_id.get(session_id)
        if session_dict is None:
            return None

        if self.session_duration <= 0:
            return session_dict.get('user_id')

        created_at = datetime.fromisoformat(session_dict.get('created_at'))
        if datetime.now() > created_at + timedelta(seconds=self.session_diration):
            return None

        return session_dict.get('user_id')

    def destroy_session(self, request=None):
        """ Destroy a session based on request cookie """
        if request is None:
            return False

        session_id = request.cookies.get(getenv('SESSION_NAME'))
        if session_id and session_id in self.user_id_by_session_id:
            del self.user_id_by_session_id[session_id]
            self.save_user_sessions()
            return True

        return False
