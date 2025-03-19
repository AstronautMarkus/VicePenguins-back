import jwt
from functools import wraps
from flask import request, jsonify
from app.config import Config

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

                if decoded_token.get('role_id') not in allowed_roles:
                    return jsonify({'error': 'Unauthorized access'}), 403

                request.user = {
                    "user_id": decoded_token.get("user_id"),
                    "username": decoded_token.get("username"),
                    "role_id": decoded_token.get("role_id")
                }

                return f(*args, **kwargs)
            except jwt.ExpiredSignatureError:
                return jsonify({'error': 'Token has expired'}), 401
            except jwt.InvalidTokenError:
                return jsonify({'error': 'Invalid token'}), 401

        return decorated_function
    return decorator

