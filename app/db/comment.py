#법안에 대한 댓글 저장 SQLite 테이블 생성 스크립트

import sqlite3 # SQLite DB 사용

def create_comment_table():
    conn = sqlite3.connect("acton.db") # DB 연결
    cur = conn.cursor() # 커서 생성
    cur.execute("""
        CREATE TABLE IF NOT EXISTS comments ( #댓글 테이블 생성
            id INTEGER PRIMARY KEY AUTOINCREMENT, #고유 ID
            user_id TEXT NOT NULL, #작성자 ID
            law_id TEXT NOT NULL, #대상 법안 ID 
            content TEXT NOT NULL, #댓글 내용
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP #작성 시각
        )
    """)
    conn.commit() # 저장
    conn.close() # 연결 종료

if __name__ == "__main__":
    create_comment_table() # 직접 실행 시 테이블 생성
