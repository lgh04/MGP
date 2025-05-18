from fastapi import APIRouter
from pydantic import BaseModel
from ..services.vote_service import submit_vote

router = APIRouter()

class VoteRequest(BaseModel):
    user_id: str
    law_id: str
    vote_type: str  # "yes" 또는 "no"

@router.post("/vote")
def vote_endpoint(vote: VoteRequest):
    success = submit_vote(vote.user_id, vote.law_id, vote.vote_type)
    return {"success": success}



"""
/routers/vote.py
역할:
사용자가 법안에 대해 찬반 투표를 제출하는 API 라우터.

연결된 서비스:
vote_service.py: 투표 처리 로직이 들어있는 서비스 레이어

엔드포인트 목록:
투표 제출 = 메서드-POST, 경로-/vote, 요청 스키마-VoteRequest, 응답-투표 성공 여부(success: bool)

동작 흐름 요약
/vote: 사용자 ID, 법안 ID, 투표 유형("yes" 또는 "no")을 받아 투표를 처리하고 성공 여부를 반환한다.
"""
