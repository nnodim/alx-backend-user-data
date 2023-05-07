#!/usr/bin/env python3
"""
Module of Users views
"""
import os
from api.v1.app import auth
from flask import request, jsonify, make_response, abort
from api.v1.views import app_views
from models.user import User


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def session_auth_login() -> str:
    """
    user login
    """
    email = request.form.get('email')
    password = request.form.get('password')
    if email is None or email == '':
        return make_response(jsonify({"error": "email missing"}), 400)
    if password is None or password == '':
        return make_response(jsonify({"error": "password missing"}), 400)
    users = User.search({'email': email})
    if not users or users == []:
        return jsonify({"error": "no user found for this email"}), 404
    for user in users:
        if user.is_valid_password(password):
            session_id = auth.create_session(user.id)
            response = jsonify(user.to_json())
            session_name = os.getenv('SESSION_NAME')
            response.set_cookie(session_name, session_id)
            return response
    return make_response(jsonify({"error": "wrong password"}), 401)


@app_views.route(
    '/auth_session/logout', methods=['DELETE'], strict_slashes=False)
def session_auth_logout():
    """
    User logout
    """
    if auth.destroy_session(request):
        return jsonify({}), 200
    abort(404)
