#!/usr/bin/env python3
"""
Module for SessionDButh
"""
from api.v1.auth.session_exp_auth import SessionExpAuth
from models.user_session import UserSession
from uuid import uuid4
from datetime import datetime, timedelta


class SessionDBAuth(SessionExpAuth):
    """
    SessionDBAuth class
    """

    def create_session(self, user_id=None):
        """
        Create a Session ID
        """
        session_id = super().create_session(user_id)
        if session_id:
            new_session = UserSession(
                {
                    "user_id": user_id,
                    "session_id": session_id
                }
            )
            new_session.save()
            return session_id
        return None

    def user_id_for_session_id(self, session_id=None):
        """
        Return user ID based on a session ID
        """
        if session_id is None:
            return None
        user_session = UserSession.search({'session_id': session_id})
        if user_session and self.session_duration > 0:
            created_at = user_session.created_at
            session_duration_seconds = self.session_duration
            session_expiration = created_at + \
                timedelta(seconds=session_duration_seconds)
            if session_expiration < datetime.now():
                return None
        return user_session.user_id

    def destroy_session(self, request=None):
        """
        Destroy user session
        """
        session_id = self.session_cookie(request)
        if not session_id:
            return False
        user_session = UserSession.search({'session_id': session_id})
        if not user_session:
            return False
        user_session.remove()
        return True
