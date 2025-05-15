from flask import Flask, request, jsonify, send_from_directory
from auth import verify_user, hash_password
from db import init_db
from utils import save_uploaded_file
import sqlite3
from datetime import datetime
import os

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    role = verify_user(username, password)
    if role:
        return jsonify({"status": "success", "role": role})
    return jsonify({"status": "failure"}), 401

@app.route('/announcements', methods=['GET', 'POST'])
def announcements():
    if request.method == 'POST':
        data = request.json
        title = data.get('title')
        content = data.get('content')
        date_posted = datetime.now().isoformat()
        conn = sqlite3.connect('campusconnect.db')
        c = conn.cursor()
        c.execute("INSERT INTO announcements (title, content, date_posted) VALUES (?, ?, ?)",
                  (title, content, date_posted))
        conn.commit()
        conn.close()
        return jsonify({"status": "announcement posted"})

    conn = sqlite3.connect('campusconnect.db')
    c = conn.cursor()
    c.execute("SELECT title, content, date_posted FROM announcements ORDER BY date_posted DESC")
    rows = c.fetchall()
    conn.close()
    return jsonify([{"title": r[0], "content": r[1], "date_posted": r[2]} for r in rows])

@app.route('/resources', methods=['GET', 'POST'])
def resources():
    if request.method == 'POST':
        file = request.files['file']
        uploader = request.form.get('uploader')
        filepath, upload_date = save_uploaded_file(file)
        conn = sqlite3.connect('campusconnect.db')
        c = conn.cursor()
        c.execute("INSERT INTO resources (filename, filepath, uploader, upload_date) VALUES (?, ?, ?, ?)",
                  (file.filename, filepath, uploader, upload_date))
        conn.commit()
        conn.close()
        return jsonify({"status": "file uploaded"})

    conn = sqlite3.connect('campusconnect.db')
    c = conn.cursor()
    c.execute("SELECT filename, filepath, uploader, upload_date FROM resources")
    rows = c.fetchall()
    conn.close()
    return jsonify([{"filename": r[0], "filepath": r[1], "uploader": r[2], "upload_date": r[3]} for r in rows])

@app.route('/uploads/<filename>')
def download_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
