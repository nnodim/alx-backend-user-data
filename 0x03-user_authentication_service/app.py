#!/usr/bin/env python3
"""
Flask app
"""
from flask import Flask, jsonify, request, make_response, abort
from auth import Auth

AUTH = Auth()
app = Flask(__name__)


@app.route('/', methods=['GET'])
def index() -> str:
    """
    index route
    """
    return jsonify({"message": "Bienvenue"})


@app.route('/users', methods=['POST'])
def users() -> str:
    """
    users route
    """
    email = request.form.get('email')
    password = request.form.get('password')
    try:
        user = AUTH.register_user(email, password)
        return jsonify({"email": user.email, "message": "user created"})
    except Exception:
        return jsonify({"message": "email already registered"}), 400


@app.route("/sessions", methods=["POST"])
def login():
    """
    login user
    """
    email = request.form.get("email")
    password = request.form.get("password")
    if not AUTH.valid_login(email, password):
        abort(401)
    session_id = AUTH.create_session(email)
    response = make_response(jsonify(
        {"email": email, "message": "logged in"})).set_cookie(
            "session_id", session_id
        )
    return response


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
