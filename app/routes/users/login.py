from flask import jsonify, request
from werkzeug.security import check_password_hash
from . import users
from app.utils.db_connection import MySQLConnection

@users.route('/login', methods=['POST'])
def login_user():
    db = MySQLConnection()
    try:
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')


        if not email or not password:
            return jsonify({'error': 'Email and password are required.'}), 400


        query = "SELECT id, username, email, password_hash, role_id FROM users WHERE email = %s"
        user = db.execute_query(query, (email,))

        if not user:
            return jsonify({'error': 'User not found.'}), 404

        user = user[0]  

        if not check_password_hash(user['password_hash'], password):
            return jsonify({'error': 'Incorrect password.'}), 401

        return jsonify({
            'message': 'Login successful.',
            'user': {
                'id': user['id'],
                'username': user['username'],
                'email': user['email'],
                'role_id': user['role_id']
            }
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        db.close()
