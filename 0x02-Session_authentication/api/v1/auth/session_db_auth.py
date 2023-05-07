#!/usr/bin/env python3
"""
Module for SessionDButh
"""
from .session_exp_auth import SessionExpAuth
from models.user_session import UserSession


class SessionDBAuth(SessionExpAuth):
    """
    SessionDBAuth class
    """

    def create_session(self, user_id=None):
        """
        Create a Session ID
        """
        session_id = super().create_session(user_id)
        if not session_id:
            return None
        credentials = {
                    "user_id": user_id,
                    "session_id": session_id
                }
        new_session = UserSession(credentials)
        new_session.save()
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """
        Return user ID based on a session ID
        """
        if session_id is None:
            return None
        user_session = UserSession.search({'session_id': session_id})
        if user_session:
            return user_session
        return None

    def destroy_session(self, request=None):
        """
        Destroy user session
        """
        if request is None:
            return False
        session_id = self.session_cookie(request)
        if not session_id:
            return False
        user_session = UserSession.search({'session_id': session_id})
        if not user_session:
            return False
        user_session.remove()
        return True
