# 사용자가 특정 법안에 대해 찬성 또는 반대 투표를 제출하는 라우터

from fastapi import APIRouter # FastAPI 라우터 기능
from pydantic import BaseModel  # 요청 데이터 구조 정의용
from ..services.vote_service import submit_vote # 투표 처리 로직 함수

router = APIRouter()

# 투표 요청 시 사용할 요청 본문 형식
class VoteRequest(BaseModel):
    user_id: str # 투표한 사용자 ID
    law_id: str # 대상 법안 ID
    vote_type: str  # "yes" 또는 "no" # "yes" 또는 "no"

# 사용자가 찬반 투표를 제출하면 처리하는 API
@router.post("/vote")
def vote_endpoint(vote: VoteRequest):
    success = submit_vote(vote.user_id, vote.law_id, vote.vote_type) # 서비스 로직 실행
    return {"success": success} # 성공 여부 반환
