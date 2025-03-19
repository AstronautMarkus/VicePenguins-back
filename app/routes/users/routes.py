from flask import jsonify, request
from werkzeug.security import generate_password_hash
from . import users
from app.utils.db_connection import MySQLConnection

@users.route('/')
def list_users():
    db = MySQLConnection()
    try:
        query = "SELECT id, username, email, role_id, created_at FROM users"
        users = db.execute_query(query)
        return jsonify(users), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        db.close()

@users.route('/<int:user_id>')
def get_user(user_id):
    db = MySQLConnection()
    try:
        query = "SELECT id, username, email, role_id, created_at FROM users WHERE id = %s"
        user = db.execute_query(query, (user_id,))
        if not user:
            return jsonify({'error': 'User not found.'}), 404
        return jsonify(user[0]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        db.close()

@users.route('/', methods=['POST'])
def create_user():
    db = MySQLConnection()
    try:
        data = request.get_json()
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')
        role_id = data.get('role_id')
        user_image = data.get('user_image')

        # Basic validations
        missing_fields = []
        if not username:
            missing_fields.append('username')
        if not email:
            missing_fields.append('email')
        if not password:
            missing_fields.append('password')
        if not role_id:
            missing_fields.append('role_id')

        if missing_fields:
            return jsonify({'error': 'Missing required fields.', 'missing_fields': missing_fields}), 400

        # Check if username or email already exists
        query_check_user = "SELECT id FROM users WHERE username = %s OR email = %s"
        existing_user = db.execute_query(query_check_user, (username, email))
        if existing_user:
            return jsonify({'error': 'Username or email already in use.'}), 409

        # Check if role_id exists
        query_check_role = "SELECT id FROM roles WHERE id = %s"
        existing_role = db.execute_query(query_check_role, (role_id,))
        if not existing_role:
            return jsonify({'error': 'Invalid role_id.'}), 400

        
        password_hash = generate_password_hash(password)

        
        query = """
            INSERT INTO users (username, email, password_hash, user_image, role_id)
            VALUES (%s, %s, %s, %s, %s)
        """
        db.execute_query(query, (username, email, password_hash, user_image, role_id))
        db.commit()

        return jsonify({'message': 'User created successfully.'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        db.close()
