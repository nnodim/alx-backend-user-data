#!/usr/bin/env python3
"""
Module for SessionExpAuth
"""
from api.v1.auth.auth import Auth
from datetime import datetime, timedelta
import os


class SessionExpAuth(Auth):
    """
    SessionExpAuth class
    """

    def __init__(self):
        """
        Initialize session duration
        """
        super().__init__()
        try:
            duration = int(os.getenv('SESSION_DURATION'))
        except Exception:
            duration = 0
        self.session_duration = duration


    def create_session(self, user_id=None):
        """
        Create a Session ID
        """
        session_id = super().create_session(user_id)
        if session_id is None:
            return None
        self.user_id_by_session_id[session_id] = {
            "user_id": user_id,
            "created_at": datetime.now()
        }
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """
        Return user ID based on a session ID
        """
        if session_id is None:
            return None
        session = self.user_id_by_session_id.get(session_id)
        if session is None:
            return None
        created_at = session.get('created_at')
        if not created_at:
            return None
        user_id = session.get('user_id')
        if self.session_duration <= 0:
            return user_id
        timeout_duration = created_at + timedelta(seconds=self.session_duration)
        if datetime.now() > timeout_duration:
            return None
        return user_id
