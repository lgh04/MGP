from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.responses import JSONResponse
from pydantic import BaseModel, EmailStr
from . import schemas, crud
from backend.db.database import SessionLocal, get_db
from .email_service import send_email
import random, time, re
from sqlalchemy.orm import Session
from typing import Dict

router = APIRouter()
code_storage = {}

# -------------------------------
# 유효성 검사 함수
# -------------------------------

def validate_password(password: str):
    if not re.match(r'^(?=.*[a-zA-Z])(?=.*\d)(?=.*[!@#$%^&*()_+=\-]).{8,}$', password):
        raise HTTPException(
            status_code=400,
            detail="비밀번호는 영문자, 숫자, 특수문자를 포함한 8자 이상이어야 합니다."
        )

def validate_phone(phone: str):
    if not re.fullmatch(r'\d{10,11}', phone):
        raise HTTPException(
            status_code=400,
            detail="전화번호는 숫자만 입력해야 하며 10~11자리여야 합니다."
        )

# -------------------------------
# 닉네임 중복 확인 (프론트 실시간 요청용)
# -------------------------------
@router.get("/check-nickname")
def check_nickname(nickname: str):
    db = SessionLocal()
    try:
        user = crud.get_user_by_nickname(db, nickname)
        return {"available": not bool(user)}
    finally:
        db.close()

# -------------------------------
# 회원가입
# -------------------------------
@router.post("/register")
def register_user(user: schemas.UserCreate):
    validate_password(user.password)
    validate_phone(user.phone)

    db = SessionLocal()
    try:
        if crud.get_user_by_nickname(db, user.nickname):
            raise HTTPException(status_code=400, detail="이미 사용 중인 닉네임입니다.")
        return crud.create_user(db, user)
    finally:
        db.close()

# -------------------------------
# 이메일 인증번호 전송
# -------------------------------
class EmailRequest(BaseModel):
    email: EmailStr

@router.post("/send-email-code")
def send_email_code(data: EmailRequest):
    code = str(random.randint(100000, 999999))
    try:
        print(f"[DEBUG] Sending code {code} to {data.email}")
        send_email(data.email, code)
        code_storage[data.email] = {
            "code": code,
            "expires": time.time() + 180
        }
        return JSONResponse(
            content={"message": "이메일로 인증번호 전송됨"},
            headers={
                "Access-Control-Allow-Origin": "http://localhost:3000",
                "Access-Control-Allow-Credentials": "true"
            }
        )
    except Exception as e:
        print(f"[ERROR] 이메일 전송 실패: {e}")
        return JSONResponse(
            status_code=500,
            content={"detail": str(e)},
            headers={
                "Access-Control-Allow-Origin": "http://localhost:3000",
                "Access-Control-Allow-Credentials": "true"
            }
        )

# -------------------------------
# 이메일 인증번호 확인
# -------------------------------
class VerifyRequest(BaseModel):
    email: EmailStr
    code: str

@router.post("/verify-email-code")
def verify_email_code(data: VerifyRequest):
    try:
        record = code_storage.get(data.email)
        if not record:
            return JSONResponse(
                status_code=404,
                content={"detail": "인증 기록 없음"},
                headers={
                    "Access-Control-Allow-Origin": "http://localhost:3000",
                    "Access-Control-Allow-Credentials": "true"
                }
            )
        if record["expires"] < time.time():
            return JSONResponse(
                status_code=400,
                content={"detail": "인증번호 만료"},
                headers={
                    "Access-Control-Allow-Origin": "http://localhost:3000",
                    "Access-Control-Allow-Credentials": "true"
                }
            )
        if record["code"] != data.code:
            return JSONResponse(
                status_code=400,
                content={"detail": "인증번호 불일치"},
                headers={
                    "Access-Control-Allow-Origin": "http://localhost:3000",
                    "Access-Control-Allow-Credentials": "true"
                }
            )
        return JSONResponse(
            content={"message": "이메일 인증 성공"},
            headers={
                "Access-Control-Allow-Origin": "http://localhost:3000",
                "Access-Control-Allow-Credentials": "true"
            }
        )
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"detail": str(e)},
            headers={
                "Access-Control-Allow-Origin": "http://localhost:3000",
                "Access-Control-Allow-Credentials": "true"
            }
        )

@router.post("/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)
