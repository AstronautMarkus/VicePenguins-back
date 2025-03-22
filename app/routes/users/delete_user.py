from flask import jsonify
from . import users
from app.utils.db_connection import MySQLConnection
from app.utils.auth import role_required

@users.route('/<int:user_id>', methods=['DELETE'])
@role_required(3)
def delete_user(user_id):
    db = MySQLConnection()
    try:
        query_check_user = "SELECT id FROM users WHERE id = %s"
        existing_user = db.execute_query(query_check_user, (user_id,))
        if not existing_user:
            return jsonify({'error': 'User not found.'}), 404
        query_delete_user = "DELETE FROM users WHERE id = %s"
        db.execute_query(query_delete_user, (user_id,))
        db.commit()

        return jsonify({'message': 'User deleted successfully.'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        db.close()
