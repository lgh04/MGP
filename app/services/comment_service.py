import sqlite3
from datetime import datetime

def submit_comment(user_id: str, law_id: str, content: str) -> bool:
    try:
        conn = sqlite3.connect("acton.db")
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO comments (user_id, law_id, content, created_at)
            VALUES (?, ?, ?, ?)
        """, (user_id, law_id, content, datetime.now()))
        conn.commit()
        return True
    except Exception as e:
        print("댓글 등록 실패:", e)
        return False
    finally:
        conn.close()
