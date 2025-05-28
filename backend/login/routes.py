from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.db.database import get_db
from .schemas import LoginRequest
from .crud import authenticate_user

router = APIRouter()

@router.post("/login")
def login(request: LoginRequest, db: Session = Depends(get_db)):
    user = authenticate_user(db, request.email, request.password)
    if not user:
        raise HTTPException(status_code=401, detail="이메일 또는 비밀번호가 일치하지 않습니다.")
    
    return {
        "message": "로그인 성공",
        "user_id": user.id,
        "nickname": user.nickname  # ✅ 닉네임 포함해서 응답
    }