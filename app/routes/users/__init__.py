from flask import Blueprint
from flask_cors import CORS

users = Blueprint('users', __name__)

CORS(users, supports_credentials=True)

from . import create_user, list_users, get_user, delete_user, login, create_user_mod
