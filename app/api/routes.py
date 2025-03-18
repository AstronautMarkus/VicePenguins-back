from flask import jsonify
from . import api

@api.route('/hello')
def hello():
    return jsonify({'message': 'Hello from the API blueprint!'})
