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




"""
/routers/auth.py
역할:
사용자의 인증 관련 요청을 처리하는 API 라우터.
회원가입, 로그인, 인증번호 전송 및 확인 같은 인증 흐름 전체를 담당한다.

연결된 서비스:
auth_service.py: 실제 인증 처리 로직이 들어있는 서비스 레이어
schemas/user.py: 사용자 요청을 받을 때 사용하는 데이터 구조 정의
db/get_db: SQLAlchemy 세션 의존성 주입

엔드포인트 목록:
회원가입 = 메서드-POST, 경로-/register, 요청 스키마-UserCreate, 응답-회원 생성 결과
로그인 요청 = 메서드-POST, 경로-/login, 요청 스키마-UserLogin, 응답-로그인 결과
인증번호 전송 = 메서드-POST, 경로-/auth/send-code, 요청 스키마-PhoneAuthRequest, 응답-인증번호 발송 메시지
인증번호 확인 = 메서드-POST, 경로-/auth/verify-code, 요청 스키마-PhoneAuthVerify, 응답-성공/실패 메시지

동작 흐름 요약
/register: 사용자로부터 이메일, 비밀번호, 닉네임 등을 받아 회원가입 요청을 처리한다.
/login: 이메일과 비밀번호를 입력받아 로그인 처리 후 토큰 또는 결과를 반환한다.
/auth/send-code: 사용자의 휴대폰 번호를 받아 인증번호를 생성해 저장하고 발송 메시지를 반환한다.
/auth/verify-code: 사용자가 입력한 인증번호가 DB에 저장된 값과 일치하는지 확인하고 결과를 반환한다.
"""
