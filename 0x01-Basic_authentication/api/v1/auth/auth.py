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
        return False

    def authorization_header(self, request=None) -> str:
        """
        returns the authorization header
        """
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """
        current user
        """
        return None
