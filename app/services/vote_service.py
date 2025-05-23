# 사용자가 특정 법안에 대해 찬성 또는 반대 투표를 하면 해당 정보를 데이터베이스에 저장하는 서비스 파일

import sqlite3 # SQLite 데이터베이스를 사용하기 위한 모듈
from datetime import datetime # 투표 시간 저장을 위한 datetime 모듈

# 투표 처리 함수
def submit_vote(user_id: str, law_id: str, vote_type: str) -> bool:
    try:
        conn = sqlite3.connect("acton.db") # DB 연결
        cur = conn.cursor()
        cur.execute(""" # votes 테이블에 투표 데이터 삽입
            INSERT INTO votes (user_id, law_id, vote_type, vote_time)
            VALUES (?, ?, ?, ?)
        """, (user_id, law_id, vote_type, datetime.now()))
        conn.commit() # 변경사항 커밋
        return True
    except Exception as e:
        print("투표 실패:", e) # 예외 발생 시 콘솔에 메시지 출력하고 False 반환
        return False
    finally:
        conn.close() # 연결 종료


"""
/services/vote_service.py  
역할:  
특정 사용자에 의한 법안 투표 정보를 데이터베이스에 저장하는 기능을 담당하는 서비스 레이어.  

주요 기능:  
-사용자가 특정 법안에 대해 찬성 또는 반대 투표를 제출  
-투표 정보를 DB에 저장 (`votes` 테이블)  
-투표 시간은 현재 시간으로 자동 기록  

함수 목록 및 설명:  
-def submit_vote(user_id: str, law_id: str, vote_type: str) -> bool:  
- `votes` 테이블에 `user_id`, `law_id`, `vote_type`, `vote_time` 값을 삽입  
- 실패 시 에러 메시지를 출력하고 `False` 반환  
- 성공 시 `True` 반환  

동작 흐름 요약:  
사용자 ID, 법안 ID, 투표 유형(찬성/반대)을 입력받아  
→ 현재 시간과 함께 DB에 저장  
→ 정상 저장 시 `True`, 실패 시 `False` 반환  
"""
