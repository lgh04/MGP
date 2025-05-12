from fastapi import APIRouter
from ..services.percent_service import calculate_vote_percentages
router = APIRouter()

@router.get("/vote/result/{law_id}")
def get_vote_result(law_id: str):
    result = calculate_vote_percentages(law_id)
    return result