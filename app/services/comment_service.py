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



"""
/services/comment_service.py  
역할:  
사용자가 특정 법안에 대해 작성한 댓글을 데이터베이스에 저장하는 기능을 담당하는 서비스 레이어.  

주요 기능:  
-댓글 내용을 acton.db의 `comments` 테이블에 저장  
-저장 성공 여부를 반환  

함수 목록 및 설명:  
-def submit_comment(user_id, law_id, content):  
- 주어진 user_id, law_id, 댓글 내용을 현재 시각과 함께 `comments` 테이블에 삽입  
- 저장 성공 시 True 반환, 실패 시 False 반환하며 예외 출력  

동작 흐름 요약:  
submit_comment 함수는 SQLite에 연결해 댓글 데이터를 삽입  
→ 커밋 후 연결 종료  
→ 예외 발생 시 실패 메시지를 출력하고 False 반환  
"""
