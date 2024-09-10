#!/usr/bin/env python3
""" session_auth module """

from flask import Blueprint, jsonify, request, make_response
from models.user import User
from api.v1.auth.session_auth import SessionAuth
import os
from api.v1.app import auth

api = Blueprint('api', __name__, url_prefix='/api/v1')

sa = SessionAuth()

@api.route('/auth_session/login', methods=['POST'])
def login():
    """Login route for session authentication"""
    email = request.form.get('email')
    password = request.form.get('password')

    if not email:
        return jsonify({"error": "email missing"}), 400
    if not password:
        return jsonify({"error": "password missing"}), 400

    user = User.search({"email": email})
    if not user:
        return jsonify({"error": "no user found for this email"}), 404

    user = user[0]
    if not user.is_valid_password(password):
        return jsonify({"error": "wrong password"}), 401

    session_id = sa.create_session(user.id)
    response = make_response(user.to_json())
    session_name = os.getenv("SESSION_NAME")
    response.set_cookie(session_name, session_id)

    return response

@api.route('/auth_session/logout', methods=['DELETE'])
def logout():
    """Logout route for session authentication"""
    if not auth.destroy_session(request):
        abort(404)
    return jsonify({}), 200
