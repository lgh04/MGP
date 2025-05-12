import sqlite3

def create_mypage_tables():
    conn = sqlite3.connect("acton.db")
    cur = conn.cursor()

    # 토론방 정보 테이블
    cur.execute("""
        CREATE TABLE IF NOT EXISTS discussion_rooms (
            room_id TEXT PRIMARY KEY,
            room_name TEXT NOT NULL
        )
    """)

    # 사용자-토론방 매핑 테이블
    cur.execute("""
        CREATE TABLE IF NOT EXISTS user_room_mapping (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT NOT NULL,
            room_id TEXT NOT NULL,
            UNIQUE(user_id, room_id)
        )
    """)

    conn.commit()
    conn.close()

if __name__ == "__main__":
    create_mypage_tables()
