#!/usr/bin/env python3
""" Module of SessionAuth views
"""
from flask import jsonify, abort, request
from api.v1.views import app_views
import os

from typing import Tuple
from models.user import User


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def login() -> Tuple[str, int]:
    ''' POST /api/v1/auth_session/login
    Return:
      - JSON representation of a User object.
    '''
    not_found_err = {"error": "no user found for this email"}
    email = request.form.get('email')
    if not email or len(email.strip()) == 0:
        return jsonify({"error": "email missing"}), 400
    password = request.form.get('password')
    if password is None or len(password.strip()) == 0:
        return jsonify({"error": "password missing"}), 400

    try:
        users = User.search({'email': email})
    except Exception:
        return jsonify(not_found_err), 404

    if len(users) <= 0:
        return jsonify(not_found_err), 404

    if users[0].is_valid_password(password):
        from api.v1.app import auth
        session_id = auth.create_session(getattr(users[0], 'id'))
        user = jsonify(users[0].to_json())
        user.set_cookie(os.getenv("SESSION_NAME"), session_id)
        return user
    return jsonify({"error": "wrong password"}), 401
