from flask import jsonify
from . import main

@main.route('/')
def index():
    return jsonify({'message': 'Welcome to the main blueprint!'})
