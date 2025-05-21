# 특정 법안에 대해 찬성/반대 투표 비율을 계산해 백분율로 반환하는 서비스 파일

import sqlite3 # SQLite DB 연결을 위한 모듈

# 특정 법안의 찬반 투표 비율 계산 함수
def calculate_vote_percentages(law_id: str) -> dict:
    # DB 연결
    conn = sqlite3.connect("acton.db")
    cur = conn.cursor()
    cur.execute("SELECT vote_type FROM votes WHERE law_id = ?", (law_id,)) # 해당 법안에 대한 모든 투표 결과 가져오기
    votes = cur.fetchall()
    conn.close() # 연결 종료

    total = len(votes)  # 전체 투표 수 계산
    yes_count = len([v for (v,) in votes if v == "yes"])  # "yes"인 투표 개수 계산
    no_count = total - yes_count # "no"는 전체 - yes 개수

    if total == 0: # 투표가 하나도 없으면 0%, 0% 반환
        return {"yes": 0, "no": 0}
    return { # 찬반 비율 계산 후 정수로 변환해 반환
        "yes": int((yes_count / total) * 100),
        "no": int((no_count / total) * 100)
    }



"""
/services/percent_service.py  
역할:  
특정 법안에 대한 전체 투표 결과를 바탕으로 찬반 비율(%)을 계산하는 서비스 레이어.  

주요 기능:  
-법안 ID에 해당하는 투표 결과를 DB에서 조회  
-찬성/반대 투표 비율을 계산하여 정수형 백분율로 반환  

함수 목록 및 설명:  
-def calculate_vote_percentages(law_id: str) -> dict:  
- `votes` 테이블에서 주어진 `law_id`에 대한 모든 투표 유형(`vote_type`)을 조회  
- `yes`와 `no`의 개수를 세고 전체 투표 수 대비 비율을 계산  
- 전체 투표 수가 0이면 찬반 모두 0%로 반환  
- 결과는 `{"yes": xx, "no": yy}` 형태로 반환  

동작 흐름 요약:  
법안 ID를 입력받아  
→ `votes` 테이블에서 해당 법안에 대한 모든 투표를 조회  
→ 찬성/반대 개수를 분리해 합산  
→ 전체 대비 각각의 백분율을 계산해 정수형으로 반환  
→ 투표가 없을 경우 0%로 처리  
"""
