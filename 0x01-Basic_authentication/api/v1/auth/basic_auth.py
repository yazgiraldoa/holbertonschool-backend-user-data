#!/usr/bin/env python3
"""
Class BasicAuth.
"""
import base64
from typing import Tuple, TypeVar
from api.v1.auth.auth import Auth
from models.base import Base
from models.user import User


class BasicAuth(Auth):
    """
    Class BasicAuth
    """

    def __init__(self):
        super().__init__()

    def extract_base64_authorization_header(
                                            self,
                                            authorization_header: str
                                           ) -> str:
        """Method to extract base64 authorization header"""
        if not authorization_header or \
           not isinstance(authorization_header, str) or \
           not authorization_header.startswith("Basic "):
            return None
        return authorization_header.replace("Basic ", "")

    def decode_base64_authorization_header(
                                           self,
                                           base64_authorization_header: str
                                          ) -> str:
        """Method decode base64 authorization header"""
        if not base64_authorization_header or \
           not isinstance(base64_authorization_header, str):
            return None
        try:
            str_bytes = base64_authorization_header.encode('utf-8')
            base64_bytes = base64.b64decode(str_bytes)
            return base64_bytes.decode('utf-8')
        except Exception as e:
            return None

    def extract_user_credentials(
                                 self,
                                 decoded_base64_authorization_header: str
                                ) -> Tuple[str]:
        """Method to extract user credentials"""
        if not decoded_base64_authorization_header or \
           not isinstance(decoded_base64_authorization_header, str) or \
           ':' not in decoded_base64_authorization_header:
            return (None, None)
        return tuple(decoded_base64_authorization_header.split(':'))

    def user_object_from_credentials(
                                     self,
                                     user_email: str,
                                     user_pwd: str
                                    ) -> TypeVar('User'):
        """Method that returns the User instance based on email and password"""
        if not user_email or not isinstance(user_email, str) or \
           not user_pwd or not isinstance(user_pwd, str):
            return None

        user = User()

        u = user.search({"email": user_email})
        if not u:
            return None
        p = u[0].is_valid_password(user_pwd)
        if not p:
            return None

        return u[0]
