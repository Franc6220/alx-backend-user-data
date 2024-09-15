#!/usr/bin/env python3
"""
Auth module for password hashing and to interact with the authentication database.
"""
import bcrypt
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound
import uuid

def _hash_password(password: str) -> bytes:
    """
    Hashes a password using bcrypt and returns the hashed password as bytes.

    Args:
        password (str): The password to hash.

    Returns:
        bytes: The hashed password.
    """
    # Generate a salt and hash the password using bcrypt
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

class Auth:
    """Auth class to interact with the authentication database."""

    def __init__(self):
        "create instance of db"
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """
        Registers a user with an email and password.
        If the email is already in use, raise a ValueError.

        Args:
            email (str): The user's email.
            password (str): The user's password.

        Returns:
            User: The newly created user.

        Raises:
            ValueError: If the user with the email already exists.
        """
        try:
            # Try to find if a user already exists with the provided email
            self._db.find_user_by(email=email)
            # If user is found, raise a ValueError
            raise ValueError(f"User {email} already exists")
        except NoResultFound:
            # If no result is found, we can proceed to create the user
            hashed_password = _hash_password(password)
            new_user = self._db.add_user(email, hashed_password)
            return new_user

    def valid_login(self, email: str, password: str) -> bool:
        """
        Check if a user is able to log in with the given email and password.

        Arguments:
        - email: the user's email
        - password: the plain-text password entered by the user

        Return:
        - True if the login is valid, otherwise False.
        """
        try:
            # Find the user by email
            user = self._db.find_user_by(email=email)
            # Check if the password matches
            if bcrypt.checkpw(password.encode('utf-8'), user.hashed_password):
                return True
        except NoResultFound:
            # If user is not found
            return False
        except Exception as e:
            # In case of any other exceptions (e.g., database or encoding issues)
            return False

        # If password doesn't match
        return False

    def _generate_uuid(self) -> str:
        """Generate a new UUID and return its string representation

        Returns:
            str: The string representation of a new UUID.
        """
        return str(uuid.uuid4())
