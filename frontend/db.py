import sqlite3

DB_NAME = "ids_logs.db"

def get_db():
    return sqlite3.connect(DB_NAME, check_same_thread=False)

def init_db():
    conn = get_db()
    c = conn.cursor()
    c.execute("""
    CREATE TABLE IF NOT EXISTS logs(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
        src_ip TEXT,
        dst_ip TEXT,
        prediction TEXT,
        severity TEXT,
        reason TEXT
    )
    """)
    conn.commit()
