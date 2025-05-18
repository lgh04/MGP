import sqlite3
def has_voted(user_id: str, law_id: str) -> bool:
    conn = sqlite3.connect("acton.db")
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM votes WHERE user_id = ? AND law_id = ?", (user_id, law_id))
    count = cur.fetchone()[0]
    conn.close()
    return count > 0


"""
/services/votecheck_service.py  
역할:  
특정 사용자가 특정 법안에 대해 이미 투표했는지 여부를 확인하는 서비스 레이어.  

주요 기능:  
-사용자 ID와 법안 ID를 기반으로 DB에서 해당 투표 기록 존재 여부를 확인  

함수 목록 및 설명:  
-def has_voted(user_id: str, law_id: str) -> bool:  
- `votes` 테이블에서 `user_id`와 `law_id`가 모두 일치하는 투표 기록 수를 조회  
- 조회된 수가 0보다 크면 이미 투표한 것으로 판단하여 `True` 반환  
- 그렇지 않으면 `False` 반환  

동작 흐름 요약:  
사용자 ID와 법안 ID를 입력받아  
→ DB에서 해당 조합의 투표 기록 개수를 조회  
→ 투표한 기록이 있으면 `True`, 없으면 `False` 반환  
"""
