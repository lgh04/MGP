#찬반 투표 결과를 저장하는 SQLite 테이블 생성 스크립트

import sqlite3 # SQLite 사용

def create_vote_table():
    conn = sqlite3.connect("acton.db") # DB 연결
    cur = conn.cursor() # 커서 생성
    cur.execute("""
        CREATE TABLE IF NOT EXISTS votes ( #투표 테이블 생성
            id INTEGER PRIMARY KEY AUTOINCREMENT, #고유 ID
            user_id TEXT NOT NULL, #투표한 사용자 ID
            law_id TEXT NOT NULL, #대상 법안 ID
            vote_type TEXT CHECK(vote_type IN ('yes', 'no')) NOT NULL, #찬반 여부
            vote_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP #투표 시각
        )
    """)
    conn.commit() # 저장
    conn.close() # 연결 종료

if __name__ == "__main__":
    create_vote_table() # 직접 실행 시 테이블 생성
