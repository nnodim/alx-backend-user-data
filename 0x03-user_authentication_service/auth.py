#!/usr/bin/env python3
"""
Auth file
"""
import uuid
import bcrypt
from db import DB
from user import User
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
            existing_user = self._db.find_user_by(email=email)
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
