#!/usr/bin/env python3
"""
Auth file
"""
import bcrypt


def _hash_password(password: str) -> bytes:
    """
    hash password
    """
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode('utf-8'), salt)
