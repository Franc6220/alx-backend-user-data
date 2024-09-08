#!/usr/bin/env python3
""" BasicAuth module
"""
import base64
from api.v1.auth.auth import Auth

class BasicAuth(Auth):
    """ BasicAuth class that inherits from Auth """
    
    def extract_base64_authorization_header(self, authorization_header: str) -> str:
        """
        Extract the Base64 part of the Authorization header for Basic Authentication.

        Args:
            authorization_header (str): The Authorization header from the request.

        Returns:
            str: The Base64 part of the header, or None if the conditions are not met.
        """
        if authorization_header is None:
            return None
        if not isinstance(authorization_header, str):
            return None
        if not authorization_header.startswith("Basic "):
            return None
        return authorization_header[len("Basic "):]

    def decode_base64_authorization_header(self, base64_authorization_header: str) -> str:
        """
        Decode a Base64 string and return the decoded value as a UTF-8 string.

        Args:
            base64_authorization_header (str): The Base64 string to decode.

        Returns:
            str: The decoded string, or None if the input is invalid.
        """
        if base64_authorization_header is None:
            return None
        if not isinstance(base64_authorization_header, str):
            return None

        try:
            # Ensure that Base64 is correctly padded
            missing_padding = len(base64_authorization_header) % 4
            if missing_padding != 0:
                base64_authorization_header += '=' * (4 - missing_padding)

            # Decode Base64 and return as UTF-8 string, stripping unnecessary padding or spaces
            decoded_bytes = base64.b64decode(base64_authorization_header, validate=True)
            return decoded_bytes.decode('utf-8')
        except (base64.binascii.Error, ValueError, TypeError):
            return None

    def extract_user_credentials(self, decoded_base64_authorization_header: str) -> (str, str):
        """
        Extract the user email and password from the Base64 decoded value.

        Args:
            decoded_base64_authorization_header (str): The decoded Base64 string.

        Returns:
            (str, str): Tuple of (user email, user password), or (None, None) if invalid.
        """
        if decoded_base64_authorization_header is None:
            return None, None

        if not isinstance(decoded_base64_authorization_header, str):
            return None, None

        if ':' not in decoded_base64_authorization_header:
            return None, None

        # Split the string into email and password
        email, password = decoded_base64_authorization_header.split(':', 1)
        return email, password
