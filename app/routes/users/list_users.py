from flask import jsonify
from . import users
from app.utils.db_connection import MySQLConnection
from app.utils.auth import role_required

@users.route('/')
@role_required([3])
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
