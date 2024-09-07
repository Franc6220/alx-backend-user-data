#!/usr/bin/env python3
""" Auth module
"""
from flask import request
from typing import List, TypeVar


class Auth:
    def __init__(self):
        """
        Initialization method for the Auth class.
        """
        # Initialize attributes here if needed
        pass

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """
        Returns False - path and excluded_paths will be used later
        """
        return False

    def authorization_header(self, request=None) -> str:
        """
        Returns None - request will be the Flask request object
        """
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """
        Returns None - request will be the Flask request object
        """
        return None
