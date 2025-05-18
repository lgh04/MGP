# 법안 정보를 저장하는 SQLite 테이블 생성 스크립트

import sqlite3 # SQLite DB 사용

def create_law_table():
    conn = sqlite3.connect("acton.db") # DB 연결
    cur = conn.cursor() # 커서 생성
    cur.execute("""
        CREATE TABLE IF NOT EXISTS laws ( #법안 테이블 생성
            law_id TEXT PRIMARY KEY, #고유 법안 ID
            title TEXT, #법안 제목
            content TEXT, #법안 내용
            last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP #마지막 수정 시각
        )
    """)
    conn.commit() # 저장
    conn.close() # 연결 종료

if __name__ == "__main__":
    create_law_table() # 직접 실행 시 테이블 생성
