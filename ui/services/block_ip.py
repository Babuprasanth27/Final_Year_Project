from db.database import get_db

def block_ip(ip):
    conn = get_db()
    conn.execute(
        "INSERT OR IGNORE INTO blocked_ips (ip, reason) VALUES (?,?)",
        (ip, "Severe attack")
    )
    conn.commit()
