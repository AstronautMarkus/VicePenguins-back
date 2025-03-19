from flask import jsonify
from . import users

@users.route('/hello')
def hello():
    return jsonify({'message': 'Hello from the API blueprint!'})
