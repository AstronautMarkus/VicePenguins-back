from flask import jsonify
from . import users
from app.utils.db_connection import MySQLConnection
from app.utils.auth import role_required

@users.route('/<int:user_id>')
@role_required([3])
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