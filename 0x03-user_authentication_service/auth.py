#!/usr/bin/env python3
"""
Auth module for password hashing
"""
import bcrypt

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
