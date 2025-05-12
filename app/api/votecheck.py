from fastapi import APIRouter
from ..services.votecheck_service import has_voted
router = APIRouter()


@router.get("/vote/check")
def check_user_vote(user_id: str, law_id: str):
    return {"voted": has_voted(user_id, law_id)}
