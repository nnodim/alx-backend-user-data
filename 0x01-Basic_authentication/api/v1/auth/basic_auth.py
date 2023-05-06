#!/usr/bin/env python3
"""
Basic auth
"""
from typing import TypeVar
from .auth import Auth
import base64

User = TypeVar('User')


class BasicAuth(Auth):
    """
    basic auth
    """

    def extract_base64_authorization_header(self,
                                            authorization_header: str) -> str:
        """
        extract_base64_authorization_header
        """
        if authorization_header is None:
            return None
        if not isinstance(authorization_header, str):
            return None

        if not authorization_header.startswith('Basic '):
            return None

        credentials = authorization_header.split(' ')[-1]
        return credentials

    def decode_base64_authorization_header(
            self, base64_authorization_header: str) -> str:
        """
        decode_base64_authorization_header
        """
        if base64_authorization_header is None:
            return None
        if not isinstance(base64_authorization_header, str):
            return None
        try:
            encoded = base64_authorization_header.encode('utf-8')
            decoded = base64.b64decode(encoded)
            return decoded.decode('utf-8')
        except Exception:
            return None

    def extract_user_credentials(
            self, decoded_base64_authorization_header: str) -> (str, str):
        """
        extract_user_credentials
        """
        if decoded_base64_authorization_header is None:
            return (None, None)
        if not isinstance(decoded_base64_authorization_header, str):
            return (None, None)
        if ':' not in decoded_base64_authorization_header:
            return None, None
        email, password = decoded_base64_authorization_header.split(':')
        return (email, password)

    def user_object_from_credentials(
            self, user_email: str, user_pwd: str) -> TypeVar('User'):
        """
        user_object_from_credentials
        """
        if user_email is None or not isinstance(user_email, str):
            return None
        if user_pwd is None or not isinstance(user_pwd, str):
            return None
        try:
            user_set = User.search({"email": user_email})
            if not user_set or user_set == []:
                return None
            for user in user_set:
                if user.is_valid_password(user_pwd):
                    return user
            return None
        except Exception:
            return None