import sqlite3

def get_user_rooms(user_id: str) -> list:
    conn = sqlite3.connect("acton.db")
    cur = conn.cursor()
    cur.execute("""
        SELECT r.room_id, r.room_name 
        FROM user_room_mapping urm
        JOIN discussion_rooms r ON urm.room_id = r.room_id
        WHERE urm.user_id = ?
    """, (user_id,))
    rows = cur.fetchall()
    conn.close()
    return [{"room_id": r[0], "room_name": r[1]} for r in rows]
