import sqlite3

def init_db():
    conn = sqlite3.connect('campusconnect.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users (
                 id INTEGER PRIMARY KEY AUTOINCREMENT,
                 username TEXT UNIQUE NOT NULL,
                 password TEXT NOT NULL,
                 role TEXT NOT NULL
                 )''')

    c.execute('''CREATE TABLE IF NOT EXISTS announcements (
                 id INTEGER PRIMARY KEY AUTOINCREMENT,
                 title TEXT NOT NULL,
                 content TEXT NOT NULL,
                 date_posted TEXT NOT NULL
                 )''')

    c.execute('''CREATE TABLE IF NOT EXISTS resources (
                 id INTEGER PRIMARY KEY AUTOINCREMENT,
                 filename TEXT NOT NULL,
                 filepath TEXT NOT NULL,
                 uploader TEXT NOT NULL,
                 upload_date TEXT NOT NULL
                 )''')

    conn.commit()
    conn.close()

if __name__ == '__main__':
    init_db()
