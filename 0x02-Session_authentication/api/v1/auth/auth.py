#!/usr/bin/env python3
""" Auth module
"""
from flask import request
from typing import List, TypeVar
import fnmatch
from os import getenv


class Auth:
    """Template for API authentication system"""

    def __init__(self):
        """
        Initialization method for the Auth class.
        """
        pass

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """
        Determine if authentication is required for the given path.
        Returns True if path is not in the list of strings excluded_paths.

        Args:
            path (str): The path to check.
            excluded_paths (List[str]): List of paths that are excluded from authentication.

        Returns:
            bool: True or False depending on the conditions.
        """
        if path is None:
            return True

        if excluded_paths is None or len(excluded_paths) == 0:
            return True

        # Normalize path to ensure consistency in comparison
        path = path.rstrip('/') + '/'
        
        for excluded_path in excluded_paths:
            # Normalize excluded path
            normalized_excluded_path = excluded_path.rstrip('/') + '/'
            if fnmatch.fnmatch(path, normalized_excluded_path):
                return False

        return True

    def authorization_header(self, request=None) -> str:
        """
        Get the authorization header from the request.
        For now, it always returns None.

        Args:
            request (Flask request): The Flask request object.

        Returns:
            str: None (no authorization header).
        """
        if request is None:
            return None
        return request.headers.get('Authorization', None)

    def current_user(self, request=None) -> TypeVar('User'):
        """
        Get the current user from the request.
        For now, it always returns None.

        Args:
            request (Flask request): The Flask request object.

        Returns:
            User: None (no current user).
        """
        return None

    def session_cookie(self, request=None):
        """
        Return the value of the session cookie named by the environment variable SESSION_NAME.

        Args:
            request (Flask request): The Flask request object.

        Returns:
            str: The value of the session cookie, or None if not found.
        """
        if request is None:
            return None

        # Get the session cookie name from the environment variable or default to '_my_session_id'
        session_name = getenv('SESSION_NAME', '_my_session_id')
        return request.cookies.get(session_name)
