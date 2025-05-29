from fastapi import APIRouter, HTTPException
from . import crud, schemas  # ✅ 상대 경로로 수정

router = APIRouter()

@router.get("/law/{bill_id}", response_model=schemas.LawDetail)
def get_law_detail(bill_id: str):
    try:
        law_data = crud.fetch_law_detail_from_api(bill_id)
        return law_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
