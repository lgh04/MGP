from fastapi import APIRouter
from app.services.law_service import fetch_law_detail

router = APIRouter()

@router.get("/law/{law_id}")
def get_law_detail(law_id: str):
    return fetch_law_detail(law_id)
