from flask import jsonify
from . import stats
from app.utils.db_connection import MySQLConnection
from app.utils.auth import role_required

@stats.route('/', methods=['GET'])
@role_required([3])
def get_stats():
    try:
        db = MySQLConnection()

        stats_data = db.execute_query("""
            SELECT total_mods, users_active, total_views, mods_in_review, notifications, updated_at
            FROM mod_stats
            ORDER BY updated_at DESC
            LIMIT 1
        """)

        if not stats_data:
            return jsonify({"message": "No statistics available"}), 404

        return jsonify(stats_data[0]), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

    finally:
        db.close()
