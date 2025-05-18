# 특정 사용자가 특정 법안에 이미 투표했는지 여부를 확인하는 라우터
 
from fastapi import APIRouter # FastAPI 라우터 기능
from ..services.votecheck_service import has_voted # 투표 여부 확인 함수

router = APIRouter()

# 특정 사용자가 특정 법안에 투표했는지 확인하는 API
@router.get("/vote/check")
def check_user_vote(user_id: str, law_id: str):
    return {"voted": has_voted(user_id, law_id)}
