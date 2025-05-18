#FastAPI에서 회원가입·로그인·휴대폰 인증 기능 처리 라우터 파일

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..schemas.user import UserCreate, UserLogin, PhoneAuthRequest, PhoneAuthVerify
from ..services import auth_service # 실제 로직 처리 서비스
from app.db import get_db # DB 세션 연결 함수

router = APIRouter() # 라우터 인스턴스 생성

# 회원가입 API: POST /register
@router.post("/register")
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    return auth_service.create_user(user, db)

# 로그인 API: POST /login
@router.post("/login")
def login_user(user: UserLogin, db: Session = Depends(get_db)):
    return auth_service.authenticate_user(user, db)

# 인증번호 전송 API: POST /auth/send-code
@router.post("/auth/send-code")
def send_code(request: PhoneAuthRequest, db: Session = Depends(get_db)):
    return {"message": f"인증번호 {auth_service.generate_auth_code(request.phone, db)}가 발송되었습니다."}

# 인증번호 확인 API: POST /auth/verify-code
@router.post("/auth/verify-code")
def verify_code(request: PhoneAuthVerify, db: Session = Depends(get_db)):
    if auth_service.verify_auth_code(request.phone, request.input_code, db):
        return {"message": "인증 성공"}
    raise HTTPException(status_code=400, detail="인증번호가 일치하지 않습니다.")
