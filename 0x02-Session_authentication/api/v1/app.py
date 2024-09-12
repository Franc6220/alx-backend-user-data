#!/usr/bin/env python3
"""
Route module for the API
"""
from os import getenv
from api.v1.auth.auth import Auth
from api.v1.views import app_views
from api.v1.auth.basic_auth import BasicAuth
from api.v1.auth.session_auth import SessionAuth
from api.v1.auth.session_exp_auth import SessionExpAuth
from flask import Flask, jsonify, abort, request
from flask_cors import (CORS, cross_origin)
import os


app = Flask(__name__)
app.register_blueprint(app_views)
CORS(app, resources={r"/api/v1/*": {"origins": "*"}})

auth = None

# Load the correct authentication system based on the AUTH_TYPE environment variable
auth_type = getenv('AUTH_TYPE')
if auth_type == "basic_auth":
    auth = BasicAuth()
elif auth_type == "session_auth":
    auth = SessionAuth()
elif auth_type == "session_exp_auth":
    auth = SessionExpAuth()
else:
    auth = Auth()

@app.before_request
def before_request() -> None:
    """Filter all requests and set the current_user"""
    if auth is None:
        return

    excluded_paths = [
            '/api/v1/status/',
            '/api/v1/unauthorized/',
            '/api/v1/forbidden/',
            '/api/v1/auth_session/login/'
            ]

    if not auth.require_auth(request.path, excluded_paths):
        return

    if auth.authorization_header(request) is None and auth.session_cookie(request) is None:
        abort(401)

    current_user = auth.current_user(request)
    if current_user is None:
        abort(403)   # Forbidden

    # Set the current user in the request object
    request.current_user = current_user

@app.errorhandler(404)
def not_found(error) -> str:
    """ Not found handler
    """
    return jsonify({"error": "Not found"}), 404

@app.errorhandler(401)
def unauthorized_error(error) -> str:
    """ Unauthorized error handler
    """
    return jsonify({"error": "Unauthorized"}), 401

@app.errorhandler(403)
def forbidden(error) -> str:
    """ Forbidden handler
    """
    return jsonify({"error": "Forbidden"}), 403


if __name__ == "__main__":
    host = getenv("API_HOST", "0.0.0.0")
    port = getenv("API_PORT", "5000")
    app.run(host=host, port=port)
