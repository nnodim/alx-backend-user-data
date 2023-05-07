#!/usr/bin/env python3
"""
Moduule for UserSession
"""
from models.base import Base


class UserSession(Base):
    """
    UserSession class
    """
    __tablename__ = 'user_sessions'

    def __init__(self, *args: list, **kwargs: dict):
        """
        initialize class
        """
        super().__init__(*args, **kwargs)
        self.user_id = kwargs.get('user_id')
        self.session_id = kwargs.get('session_id')
