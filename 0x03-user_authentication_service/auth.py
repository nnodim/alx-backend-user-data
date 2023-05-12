#!/usr/bin/env python3
"""
Auth file
"""
import uuid
import bcrypt
from db import DB
from user import User
from typing import Optional
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import IntegrityError


def _hash_password(password: str) -> bytes:
    """
    hash password
    """
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode('utf-8'), salt)


def _generate_uuid() -> str:
    """
    Generate a new UUID
    """
    id = str(uuid.uuid4())
    return id


class Auth:
    """Auth class
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """
        Register user
        """
        try:
            user = self._db.find_user_by(email=email)
            raise ValueError(f"User {email} already exists")
        except NoResultFound:
            hashed_password = _hash_password(password)

            return self._db.add_user(email, hashed_password)

    def valid_login(self, email: str, password: str) -> bool:
        """
        Valid login
        """
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            return False
        hashed_password = user.hashed_password
        return bcrypt.checkpw(password.encode('utf-8'), hashed_password)

    def create_session(self, email: str) -> str:
        """
        Create session
        """
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            return None
        else:
            session_id = _generate_uuid()
            user.session_id = session_id
            return session_id

    def get_user_from_session_id(self, session_id: str) -> Optional[User]:
        """
        get user from session id
        """
        if not session_id:
            return None
        try:
            user = self._db.find_user_by(session_id=session_id)
            return user
        except NoResultFound:
            return None

    def destroy_session(self, user_id: str) -> None:
        """
        Destroy session
        """
        try:
            user = self._db.find_user_by(user_id=user_id)
        except NoResultFound:
            return None
        else:
            user.session_id = None
            return None

    def get_reset_password_token(self, email: str) -> str:
        """
        Generates a reset password token
        """
        user = self._db.find_user_by(email=email)
        if not user:
            raise ValueError("User not found")
        password_reset_token = _generate_uuid()
        self._db.update_user(
            user.id, password_reset_token=password_reset_token)
        return password_reset_token
