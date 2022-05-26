#!/usr/bin/env python3
"""
Class to manage the API authentication.
"""
from typing import List, TypeVar
from os import getenv


class Auth:
    """
    Class to manage the API authentication
    """

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """Method that review if a path requires authentication"""
        if path is None or excluded_paths is None or len(excluded_paths) == 0:
            return True
        elif path in excluded_paths or path + '/' in excluded_paths:
            return False

        for e_path in excluded_paths:
            if '*' in e_path:
                e_path = e_path.replace('*', '')
                if path.startswith(e_path):
                    return False

        if path not in excluded_paths or path + '/' not in excluded_paths:
            return True

    def authorization_header(self, request=None) -> str:
        """Method that checks if a request has Authorization header"""
        if request is None or "Authorization" not in request.headers:
            return None
        return request.headers["Authorization"]

    def current_user(self, request=None) -> TypeVar('User'):
        """Current user method"""
        return None

    def session_cookie(self, request=None):
        """Method that returns a cookie value from a request"""
        if not request:
            return None
        session_name = getenv("SESSION_NAME")
        return request.cookies.get(session_name)
