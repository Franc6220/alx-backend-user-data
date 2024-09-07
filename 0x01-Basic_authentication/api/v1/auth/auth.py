#!/usr/bin/env python3
""" Auth module
"""
from flask import request
from typing import List, TypeVar


class Auth:
    """Template for API authentication system"""

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

        # Ensure all paths end with a '/'
        path = path.rstrip('/') + '/'
        normalized_excluded_paths = [ep.rstrip('/') + '/' for ep in excluded_paths]

        return path not in normalized_excluded_paths

    def authorization_header(self, request=None) -> str:
        """
        Get the authorization header from the request.
        For now, it always returns None.

        Args:
            request (Flask request): The Flask request object.

        Returns:
            str: None (no authorization header).
        """
        return None

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
