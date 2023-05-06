#!/usr/bin/env python3
"""
Authentication
"""
import os
from typing import List, TypeVar
from flask import request


class Auth:
    """
    manage API auth
    """

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """
        Determines whether a given path requires authentication or not
        """
        if path is None:
            return True
        if excluded_paths is None or len(excluded_paths) == 0:
            return True
        for excluded_path in excluded_paths:
            if excluded_path.startswith(path):
                return False
            elif path.startswith(excluded_path):
                return False
            elif excluded_path.endswith('*'):
                if path.startswith(excluded_path[:-1]):
                    return False
            elif path == excluded_path:
                return False
        return True

    def authorization_header(self, request=None) -> str:
        """
        returns the authorization header
        """
        if request is None:
            return None
        authentication_header = request.headers.get('Authorization')
        if authentication_header is None:
            return None
        return authentication_header

    def current_user(self, request=None) -> TypeVar('User'):
        """
        current user
        """
        return None

    def session_cookie(self, request=None):
        """
        session cookie
        """
        if request is None:
            return None
        sessionName = os.environ.get("SESSION_NAME")
        return request.cookies.get(sessionName)
