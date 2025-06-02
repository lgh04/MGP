from fastapi import APIRouter, HTTPException
from .crud import fetch_law_detail
from .schemas import LawDetail  # ✅ 여기 수정

router = APIRouter()

@router.get("/law/{bill_id}", response_model=LawDetail)
def get_law_detail(bill_id: str):
    law = fetch_law_detail(bill_id)
    if not law:
        raise HTTPException(status_code=404, detail="법안 정보를 찾을 수 없습니다.")
    return law