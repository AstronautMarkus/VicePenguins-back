from flask import jsonify, request
from . import stats
from app.utils.db_connection import MySQLConnection
from app.utils.auth import role_required

@stats.route('/save_stats', methods=['POST'])
@role_required([3])
def save_stats():
    try:
        db = MySQLConnection()

        total_mods = db.execute_query("SELECT COUNT(*) AS count FROM mod_posts")[0]['count']
        users_active = db.execute_query("SELECT COUNT(DISTINCT username) AS count FROM users")[0]['count']
        total_views = db.execute_query("SELECT SUM(views) AS total FROM mod_posts")[0]['total'] or 0

        in_review_status_id = db.execute_query("SELECT id FROM statuses WHERE name = 'in_review'")[0]['id']
        mods_in_review = db.execute_query(
            "SELECT COUNT(*) AS count FROM mod_posts WHERE status_id = %s", (in_review_status_id,)
        )[0]['count']

        notifications = db.execute_query(
            "SELECT COUNT(*) AS count FROM notifications WHERE is_read = 0"
        )[0]['count']

        db.execute_query("""
            INSERT INTO mod_stats (total_mods, users_active, total_views, mods_in_review, notifications)
            VALUES (%s, %s, %s, %s, %s)
        """, (total_mods, users_active, total_views, mods_in_review, notifications))

        db.commit()

        return jsonify({"message": "Statistics saved successfully"}), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500

    finally:
        db.close()