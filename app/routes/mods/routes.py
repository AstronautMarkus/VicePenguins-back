from flask import jsonify
from . import mods

@mods.route('/hello')
def hello():
    return jsonify({'message': 'Hello from the API blueprint!'})
