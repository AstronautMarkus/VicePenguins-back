from flask import jsonify, request
from werkzeug.security import generate_password_hash
from . import users
from app.utils.db_connection import MySQLConnection

@users.route('/', methods=['POST'])
def register_user():
    db = MySQLConnection()
    try:
        data = request.get_json()
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')
        user_image = data.get('user_image')

        missing_fields = [field for field in ['username', 'email', 'password'] if not data.get(field)]
        if missing_fields:
            return jsonify({'error': 'Missing required fields.', 'missing_fields': missing_fields}), 400


        query_check_user = "SELECT id FROM users WHERE username = %s OR email = %s"
        existing_user = db.execute_query(query_check_user, (username, email))
        if existing_user:
            return jsonify({'error': 'Username or email already in use.'}), 409


        password_hash = generate_password_hash(password)


        role_id = 1  

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
