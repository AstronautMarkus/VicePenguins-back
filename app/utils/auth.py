import jwt
from functools import wraps
from flask import request, jsonify
from app.config import Config
from app.utils.db_connection import MySQLConnection

def role_required(allowed_roles):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            token = request.headers.get('Authorization')
            if not token:
                return jsonify({'error': 'Token is missing!'}), 401
            
            try:
                token = token.split("Bearer ")[-1]
                decoded_token = jwt.decode(token, Config.SECRET_KEY, algorithms=['HS256'])
                user_id = decoded_token.get("user_id")

                if not user_id:
                    return jsonify({'error': 'Invalid token'}), 401

                db = MySQLConnection()
                query = "SELECT role_id FROM users WHERE id = %s"
                user_data = db.execute_query(query, (user_id,))
                db.close()

                if not user_data:
                    return jsonify({'error': 'User not found'}), 404

                user_role = user_data[0]['role_id']
                
                if user_role not in allowed_roles:
                    return jsonify({'error': 'Unauthorized access'}), 403

                request.user = {
                    "user_id": user_id,
                    "role_id": user_role
                }

                return f(*args, **kwargs)
            except jwt.ExpiredSignatureError:
                return jsonify({'error': 'Token has expired'}), 401
            except jwt.InvalidTokenError:
                return jsonify({'error': 'Invalid token'}), 401

        return decorated_function
    return decorator
