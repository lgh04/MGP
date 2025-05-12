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
