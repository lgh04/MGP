import sqlite3

def get_user_rooms(user_id: str) -> list:
    conn = sqlite3.connect("acton.db")
    cur = conn.cursor()
    cur.execute("""
        SELECT r.room_id, r.room_name 
        FROM user_room_mapping urm
        JOIN discussion_rooms r ON urm.room_id = r.room_id
        WHERE urm.user_id = ?
    """, (user_id,))
    rows = cur.fetchall()
    conn.close()
    return [{"room_id": r[0], "room_name": r[1]} for r in rows]


"""
/services/mypage_service.py  
역할:  
사용자의 마이페이지에서 참여 중인 토론방 목록을 조회하는 기능을 담당하는 서비스 레이어.  

주요 기능:  
-사용자가 참여한 토론방 목록을 데이터베이스에서 조회  
-토론방 ID와 이름을 포함한 리스트 형태로 반환  

함수 목록 및 설명:  
-def get_user_rooms(user_id: str) -> list:  
- `user_room_mapping` 테이블과 `discussion_rooms` 테이블을 조인하여  
  주어진 사용자 ID와 매칭된 모든 토론방 정보를 조회  
- 조회된 결과를 `room_id`와 `room_name`이 포함된 딕셔너리 리스트로 가공해 반환  

동작 흐름 요약:  
사용자 ID를 기반으로  
→ `user_room_mapping`에서 매칭된 room_id를 조회  
→ 해당 room_id를 가진 `discussion_rooms`의 이름과 함께 조인  
→ 최종적으로 `[{"room_id": ..., "room_name": ...}, ...]` 형식으로 반환  
"""
