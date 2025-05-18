import sqlite3 # SQLite 사용

def create_mypage_tables():
    conn = sqlite3.connect("acton.db") # DB 연결
    cur = conn.cursor() # 커서 생성

    # 토론방 정보 테이블
    cur.execute("""
        CREATE TABLE IF NOT EXISTS discussion_rooms (
            room_id TEXT PRIMARY KEY, #방 ID
            room_name TEXT NOT NULL #방 이름
        )
    """)

    # 사용자-토론방 매핑 테이블
    cur.execute("""
        CREATE TABLE IF NOT EXISTS user_room_mapping (
            id INTEGER PRIMARY KEY AUTOINCREMENT, #고유 ID
            user_id TEXT NOT NULL, #사용자 ID
            room_id TEXT NOT NULL, #방 ID
            UNIQUE(user_id, room_id) #중복 참여 방지
        )
    """)

    conn.commit() # 저장
    conn.close() # 연결 종료

if __name__ == "__main__":
    create_mypage_tables() # 직접 실행 시 테이블 생성
