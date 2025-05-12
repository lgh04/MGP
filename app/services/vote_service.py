import sqlite3
from datetime import datetime

def submit_vote(user_id: str, law_id: str, vote_type: str) -> bool:
    try:
        conn = sqlite3.connect("acton.db")
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO votes (user_id, law_id, vote_type, vote_time)
            VALUES (?, ?, ?, ?)
        """, (user_id, law_id, vote_type, datetime.now()))
        conn.commit()
        return True
    except Exception as e:
        print("투표 실패:", e)
        return False
    finally:
        conn.close()
