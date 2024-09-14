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

    user = User.query.filter_by(email=email).first()
    if user:
        return jsonify({"message": f"User {email} already existst"}), 400

    hashed_password = hash_password(password)
    new_user = User(email=email, hashed_password=hashed_password)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"email": email, "message": "user created"}), 201


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
