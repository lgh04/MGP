import sqlite3
def has_voted(user_id: str, law_id: str) -> bool:
    conn = sqlite3.connect("acton.db")
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM votes WHERE user_id = ? AND law_id = ?", (user_id, law_id))
    count = cur.fetchone()[0]
    conn.close()
    return count > 0
