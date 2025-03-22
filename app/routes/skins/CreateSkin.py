import os
from flask import request, jsonify, redirect, url_for
from werkzeug.utils import secure_filename
from . import skins
from app.utils.db_connection import MySQLConnection
from app.utils.auth import role_required
from dotenv import load_dotenv

load_dotenv()

UPLOAD_FOLDER = os.getenv('UPLOAD_FOLDER')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@skins.route('/create', methods=['POST'])
@role_required([3])   
def create_skin():
    user_id = request.form.get('user_id')
    if not user_id:
        return jsonify({"error": "Missing user_id"}), 400

    if 'file' not in request.files:
        return jsonify({"error": "No file part in the request"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(UPLOAD_FOLDER, filename)
        try:
            file.save(file_path)
        except Exception as e:
            return jsonify({"error": f"Failed to save file: {str(e)}"}), 500

        db = MySQLConnection()
        query = """
            INSERT INTO skins (name, filename, author_id, created_at) 
            VALUES (%s, %s, %s, NOW())
        """
        try:
            db.execute_query(query, (request.form.get('name'), filename, user_id))
            return jsonify({"message": "Skin created successfully"}), 201
        except Exception as e:
            return jsonify({"error": f"Database error: {str(e)}"}), 500
        finally:
            db.close()
    else:
        return jsonify({"error": "File type not allowed"}), 400
