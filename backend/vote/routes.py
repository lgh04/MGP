from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from backend.db.database import get_db
from . import crud
from typing import Optional
from backend.user.auth import get_current_user
from backend.db.models import User
from pydantic import BaseModel

router = APIRouter(
    prefix="/api",
    tags=["vote"]
)

class VoteRequest(BaseModel):
    vote_type: str

@router.get("/vote/{bill_id}")
def get_vote_status(
    bill_id: str, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """특정 법안의 투표 현황을 조회합니다."""
    return crud.get_vote_count(db, bill_id)

@router.post("/vote/{bill_id}")
async def vote(
    bill_id: str,
    vote_data: VoteRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """투표를 생성하거나 업데이트합니다."""
    try:
        if not vote_data.vote_type:
            raise HTTPException(status_code=400, detail="투표 유형이 지정되지 않았습니다.")
            
        if vote_data.vote_type not in ['agree', 'disagree']:
            raise HTTPException(status_code=400, detail="유효하지 않은 투표 유형입니다.")
            
        if not current_user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="로그인이 필요합니다.",
                headers={"WWW-Authenticate": "Bearer"},
            )
            
        crud.create_or_update_vote(db, bill_id, current_user.id, vote_data.vote_type)
        return crud.get_vote_count(db, bill_id)
    except Exception as e:
        print(f"Vote error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="투표 처리 중 오류가 발생했습니다."
        )

@router.get("/vote/{bill_id}/user")
async def get_user_vote_status(
    bill_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """사용자의 특정 법안에 대한 투표 여부를 조회합니다."""
    try:
        if not current_user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="로그인이 필요합니다.",
                headers={"WWW-Authenticate": "Bearer"},
            )
            
        vote = crud.get_user_vote(db, bill_id, current_user.id)
        return {"vote_type": vote.vote_type if vote else None}
    except Exception as e:
        print(f"Get user vote error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="투표 조회 중 오류가 발생했습니다."
        ) 