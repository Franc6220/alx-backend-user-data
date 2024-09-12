#!/usr/bin/env python3
""" UserSession model """

from models.base import Base
from uuid import uuid4

class UserSession(Base):
    """ UserSession class to store session data """

    def __init__(self, *args: list, **kwargs: dict):
        """ Initialize UserSession """
        self.user_id = kwargs.get('user_id', str(uuid4()))
        self.session_id = kwargs.get('session_id', str(uuid4()))
        super().__init__(*args, **kwargs)
