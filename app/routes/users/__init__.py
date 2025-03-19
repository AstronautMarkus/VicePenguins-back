from flask import Blueprint

users = Blueprint('users', __name__)

from . import create_user, list_users, get_user, delete_user
