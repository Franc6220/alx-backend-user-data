#!/usr/bin/env python3
"""
Basic Flask app for returning a JSON response and for user registration
"""

from flask import Flask, request, jsonify
from auth import Auth

app = Flask(__name__)

# Initialize the Auth object
AUTH = Auth()

@app.route("/", methods=["GET"])
def index():
    """Returns a welcome message in JSON format"""
    return jsonify({"message": "Bienvenue"})

@app.route("/users", methods=["POST"])
def register_user():
    """Register a new user"""
    email = request.form.get("email")
    password = request.form.get("password")

    if not email or not password:
        return jsonify({"message": "Missing email or password"}), 400

    try:
        # Attempt to register the user
        user = AUTH.register_user(email, password)
        return jsonify({"email": user.email, "message": "user created"})
    except ValueError as e:
        # If user already exists or another error occurs
        return jsonify({"message": str(e)}), 400


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
