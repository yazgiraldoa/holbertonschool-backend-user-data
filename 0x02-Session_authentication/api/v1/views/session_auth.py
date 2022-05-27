#!/usr/bin/env python3
""" Module of Session views
"""
from flask import jsonify, request
from api.v1.views import app_views
from models.user import User
from os import getenv


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def login():
    """ POST /auth_session/login
    Return:
      - Dictionary representation of a User
    """
    email = request.form.get('email')
    password = request.form.get('password')

    if not email or email == '':
        return jsonify({"error": "email missing"}), 400
    elif not password or password == '':
        return jsonify({"error": "password missing"}), 400

    user = User()

    u = user.search({"email": email})
    if not u:
        return jsonify({"error": "no user found for this email"}), 404
    p = u[0].is_valid_password(password)
    if not p:
        return jsonify({"error": "wrong password"}), 401
    else:
        from api.v1.app import auth
        session_id = auth.create_session(u[0].id)
        out = jsonify(u[0].to_json())
        out.set_cookie(getenv('SESSION_NAME'), session_id)
        return out
