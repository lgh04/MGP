import sqlite3
from datetime import datetime

def send_message(user_id: str, room_id: str, message: str) -> bool:
    try:
        conn = sqlite3.connect("acton.db")
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO chat_messages (user_id, room_id, message, sent_at)
            VALUES (?, ?, ?, ?)
        """, (user_id, room_id, message, datetime.now()))
        conn.commit()
        return True
    except Exception as e:
        print("메시지 전송 실패:", e)
        return False
    finally:
        conn.close()

def get_chat_history(room_id: str) -> list:
    conn = sqlite3.connect("acton.db")
    cur = conn.cursor()
    cur.execute("""
        SELECT user_id, message, sent_at 
        FROM chat_messages 
        WHERE room_id = ? 
        ORDER BY sent_at ASC
    """, (room_id,))
    rows = cur.fetchall()
    conn.close()
    return [{"user_id": r[0], "message": r[1], "sent_at": r[2]} for r in rows]
