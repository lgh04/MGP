from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..schemas.user import UserCreate, UserLogin, PhoneAuthRequest, PhoneAuthVerify
from ..services import auth_service
from app.db import get_db

router = APIRouter()

# ✅ 회원가입
@router.post("/register")
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    return auth_service.create_user(user, db)

# ✅ 로그인
@router.post("/login")
def login_user(user: UserLogin, db: Session = Depends(get_db)):
    return auth_service.authenticate_user(user, db)

# ✅ 인증번호 전송
@router.post("/auth/send-code")
def send_code(request: PhoneAuthRequest, db: Session = Depends(get_db)):
    return {"message": f"인증번호 {auth_service.generate_auth_code(request.phone, db)}가 발송되었습니다."}

# ✅ 인증번호 확인
@router.post("/auth/verify-code")
def verify_code(request: PhoneAuthVerify, db: Session = Depends(get_db)):
    if auth_service.verify_auth_code(request.phone, request.input_code, db):
        return {"message": "인증 성공"}
    raise HTTPException(status_code=400, detail="인증번호가 일치하지 않습니다.")