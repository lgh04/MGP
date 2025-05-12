from sqlalchemy.orm import Session
from fastapi import HTTPException
from ..models.user import User
from app.models.user import AuthCode as AuthModel
from ..schemas.user import UserLogin
import bcrypt, random

# ✅ 이메일 중복 및 형식 확인
def input_email(email: str, db: Session):
    if "@" not in email or "." not in email:
        raise HTTPException(status_code=400, detail="이메일 형식이 올바르지 않습니다.")
    if db.query(User).filter(User.email == email).first():
        raise HTTPException(status_code=400, detail="이미 사용 중인 이메일입니다.")

# ✅ 비밀번호 유효성 검사
def input_password(password: str):
    if len(password) < 8 or not any(c in password for c in "!@#$%^&*"):
        raise HTTPException(status_code=400, detail="비밀번호는 특수문자 포함 8자 이상이어야 합니다.")

# ✅ 이메일로 사용자 검색
def find_user_by_email(email: str, db: Session):
    return db.query(User).filter(User.email == email).first()

# ✅ 로그인 오류 처리
def handle_login_error(reason: str):
    raise HTTPException(status_code=401, detail=reason)

# ✅ 세션 저장 대체 반환
def set_session(user_id: int):
    return {"user_id": user_id}

# ✅ 회원가입 처리 함수
def create_user(user_data, db: Session):
    if db.query(User).filter(User.nickname == user_data.nickname).first():
        raise HTTPException(status_code=400, detail="이미 사용 중인 닉네임입니다.")
    input_email(user_data.email, db)
    input_password(user_data.password)
    if user_data.password != user_data.confirm_password:
        raise HTTPException(status_code=400, detail="비밀번호가 일치하지 않습니다.")
    if not verify_auth_code(user_data.phone, user_data.phone_auth_code, db):
        raise HTTPException(status_code=400, detail="휴대폰 인증이 완료되지 않았습니다.")

    hashed_pw = bcrypt.hashpw(user_data.password.encode(), bcrypt.gensalt()).decode()
    new_user = User(
        name=user_data.name,
        phone=user_data.phone,
        email=user_data.email,
        password=hashed_pw,
        nickname=user_data.nickname
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return set_session(new_user.id)

# ✅ 로그인 처리 함수
def authenticate_user(user: UserLogin, db: Session):
    db_user = find_user_by_email(user.email, db)
    if not db_user:
        handle_login_error("존재하지 않는 이메일입니다.")
    if not bcrypt.checkpw(user.password.encode(), db_user.password.encode()):
        handle_login_error("비밀번호가 일치하지 않습니다.")
    return set_session(db_user.id)

# ✅ 인증번호 생성

def generate_auth_code(phone: str, db: Session):
    code = str(random.randint(100000, 999999))
    db_code = AuthModel.AuthCode(phone=phone, code=code)
    db.add(db_code)
    db.commit()
    return code

# ✅ 인증번호 확인
def verify_auth_code(phone: str, input_code: str, db: Session):
    record = db.query(AuthModel.AuthCode).filter_by(phone=phone).order_by(AuthModel.AuthCode.id.desc()).first()
    return record and record.code == input_code
