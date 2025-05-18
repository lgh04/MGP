# 채팅 메시지용 테이블을 SQLite로 생성하는 스크립트

import sqlite3 # SQLite DB 연결용 모듈

def create_chat_table():
    conn = sqlite3.connect("acton.db") # DB 연결
    cur = conn.cursor() # 커서 생성
    cur.execute("""
        CREATE TABLE IF NOT EXISTS chat_messages ( # 테이블 없으면 생성
            id INTEGER PRIMARY KEY AUTOINCREMENT,  #고유 ID
            user_id TEXT NOT NULL, #유저 ID
            room_id TEXT NOT NULL, #방 ID
            message TEXT NOT NULL, #메시지 내용
            sent_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP #전송 시각
        )
    """)
    conn.commit() # 변경사항 저장
    conn.close() # DB 연결 종료

if __name__ == "__main__":
    create_chat_table()  # 직접 실행 시 테이블 생성
