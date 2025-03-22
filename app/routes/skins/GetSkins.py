from flask import jsonify
from . import skins
from app.utils.db_connection import MySQLConnection

@skins.route('/', methods=['GET'])
def get_skins():
    db = MySQLConnection()
    query = """
        SELECT s.id, s.name, u.username, s.filename, s.created_at 
        FROM skins s
        INNER JOIN users u ON s.id = u.id
    """
    try:
        results = db.execute_query(query)
        return jsonify(results), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        db.close()
