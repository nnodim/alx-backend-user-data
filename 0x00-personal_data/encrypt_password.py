#!/usr/bin/env python3
"""
Encrypt password
"""
import bcrypt


def hash_password(password: str) -> bytes:
    """
    Returns a hashed password
    """
    password = password.encode()
    hashed_password = bcrypt.hashpw(password, bcrypt.gensalt())
    return hashed_password
