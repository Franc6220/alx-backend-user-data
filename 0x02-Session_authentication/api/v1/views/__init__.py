#!/usr/bin/env python3
""" DocDocDocDocDocDoc
"""
from flask import Blueprint

app_views = Blueprint("app_views", __name__, url_prefix="/api/v1")

from api.v1.views.index import *
from api.v1.views.users import *

# Import the login view and add it to the Blueprint
from api.v1.views.session_auth import login
app_views.add_url_rule('/auth_session/login', view_func=login, methods=['POST'])


User.load_from_file()
