from fastapi import APIRouter
from ..services.votecheck_service import has_voted
router = APIRouter()


@router.get("/vote/check")
def check_user_vote(user_id: str, law_id: str):
    return {"voted": has_voted(user_id, law_id)}



"""
/routers/votecheck.py
역할:
사용자가 특정 법안에 대해 이미 투표했는지 확인하는 API 라우터.

연결된 서비스:
votecheck\_service.py: 투표 여부 확인 로직이 들어있는 서비스 레이어

엔드포인트 목록:
투표 여부 확인 = 메서드-GET, 경로-/vote/check, 쿼리 파라미터-user\_id(str), law\_id(str), 응답-투표 여부(voted: bool)

동작 흐름 요약
/vote/check: 사용자 ID와 법안 ID를 받아 해당 사용자가 그 법안에 대해 투표했는지 여부를 반환한다.
"""
