#!/usr/bin/env python3
"""
Module of Users views
"""
import os
from flask import request, jsonify, make_response
from api.v1.views import app_views
from models.user import User


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def session_auth_login() -> str:
    email = request.form.get('email')
    password = request.form.get('password')
    if email is None or email == '':
        return make_response(jsonify({"error": "email missing"}), 400)
    if password is None or password == '':
        return make_response(jsonify({"error": "password missing"}), 400)
    users = User.search({'email': email})
    for user in users:
        if user.is_valid_password(password):
            from api.v1.app import auth
            session_id = auth.create_session(user.id)
            response = jsonify(user.to_json())
            session_name = os.getenv('SESSION_NAME')
            response.set_cookie(session_name, session_id)
            return response
    return jsonify({"error": "wrong password"}), 401
