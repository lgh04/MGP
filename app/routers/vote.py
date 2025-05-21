# 사용자가 특정 법안에 대해 찬성 또는 반대 투표를 제출하는 API 라우터

from fastapi import APIRouter # FastAPI 라우터 기능 불러오기
from pydantic import BaseModel # 요청 데이터를 위한 Pydantic 모델
from ..services.vote_service import submit_vote # 투표 로직을 처리하는 서비스 함수 불러오기


# 라우터 인스턴스 생성
router = APIRouter()


# 투표 요청 데이터 모델 정의
class VoteRequest(BaseModel):
    user_id: str # 투표를 한 사용자 ID
    law_id: str  # 투표 대상 법안 ID
    vote_type: str  # "yes" 또는 "no" # 투표 유형: "yes" 또는 "no"

# 투표 제출 API
@router.post("/vote")  # POST 요청으로 /vote 경로 접근 시 실행
def vote_endpoint(vote: VoteRequest):
    # 서비스 함수에 user_id, law_id, vote_type 넘겨서 투표 처리
    success = submit_vote(vote.user_id, vote.law_id, vote.vote_type)
    # 성공 여부 반환
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
