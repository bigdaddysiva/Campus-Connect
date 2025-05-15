import sqlite3
import hashlib

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def verify_user(username, password):
    conn = sqlite3.connect('campusconnect.db')
    c = conn.cursor()
    c.execute("SELECT password, role FROM users WHERE username = ?", (username,))
    result = c.fetchone()
    conn.close()
    if result:
        stored_hash, role = result
        if hash_password(password) == stored_hash:
            return role
    return None



