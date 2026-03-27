import sqlite3

DB_NAME = "users.db"

def get_conn():
    return sqlite3.connect(DB_NAME)

def init_users():
    conn = get_conn()
    conn.execute("""
    CREATE TABLE IF NOT EXISTS users(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        password TEXT
    )
    """)
    conn.commit()

def signup(username, password):
    init_users()
    try:
        conn = get_conn()
        conn.execute(
            "INSERT INTO users(username,password) VALUES(?,?)",
            (username, password)
        )
        conn.commit()
        return True
    except:
        return False

def login(username, password):
    init_users()
    conn = get_conn()
    cur = conn.cursor()
    cur.execute(
        "SELECT * FROM users WHERE username=? AND password=?",
        (username, password)
    )
    return cur.fetchone() is not None
