#!/usr/bin/env python3
"""
Basic Flask app for returning a JSON response and for user registration
"""

from flask import Flask, request, jsonify, abort, make_response
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

@app.route('/sessions', methods=['POST'])
def login():
    """
    Handle POST requests to /sessions for user login.
    """
    email = request.form.get('email')
    password = request.form.get('password')

    if not email or not password:
        abort(400, description="Missing email or password")

    if AUTH.valid_login(email, password):
        session_id = AUTH.create_session(email)
        if session_id:
            response = make_response(
                    jsonify({"email": email, "message": "logged in"})
                    )
            response.set_cookie("session_id", session_id)
            return response
        else:
            abort(500, description="Unable to create session")
    else:
        abort(401, description="Invalid login credentials")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
