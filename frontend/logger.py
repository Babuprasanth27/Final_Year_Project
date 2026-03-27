from db import get_db

def log_attack(src, dst, label, severity, reason=""):
    conn = get_db()
    c = conn.cursor()
    c.execute("""
    INSERT INTO logs(src_ip, dst_ip, prediction, severity, reason)
    VALUES(?,?,?,?,?)
    """, (src, dst, label, severity, reason))
    conn.commit()
