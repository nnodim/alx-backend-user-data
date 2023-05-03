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
        if authorization_header is None or \
                not isinstance(authorization_header, str):
            return None

        if not authorization_header.startswith('Basic '):
            return None

        credentials = authorization_header.split(' ')[-1]
        return credentials
