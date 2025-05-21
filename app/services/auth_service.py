# 회원가입, 로그인, 이메일·비밀번호 유효성 검사, 휴대폰 인증번호 생성 및 검증 로직을 처리하는 서비스 파일

from sqlalchemy.orm import Session # SQLAlchemy의 세션 객체 불러오기 (DB 작업용)
from fastapi import HTTPException # FastAPI의 예외 처리 도구
from ..models.user import User # 사용자 모델 (DB 테이블)
from app.models.user import AuthCode as AuthModel # 휴대폰 인증번호 테이블 (AuthCode 모델)
from ..schemas.user import UserLogin # 로그인 요청 스키마
import bcrypt, random # 비밀번호 해싱 및 랜덤 숫자 생성을 위한 라이브러리

# 이메일 중복 및 형식 확인
def input_email(email: str, db: Session):
    if "@" not in email or "." not in email:
        raise HTTPException(status_code=400, detail="이메일 형식이 올바르지 않습니다.")
    if db.query(User).filter(User.email == email).first():
        raise HTTPException(status_code=400, detail="이미 사용 중인 이메일입니다.")

# 비밀번호 유효성 검사
def input_password(password: str):
    if len(password) < 8 or not any(c in password for c in "!@#$%^&*"):
        raise HTTPException(status_code=400, detail="비밀번호는 특수문자 포함 8자 이상이어야 합니다.")

# 이메일로 사용자 검색
def find_user_by_email(email: str, db: Session):
    return db.query(User).filter(User.email == email).first()

# 로그인 실패 시 예외 처리 함수
def handle_login_error(reason: str):
    raise HTTPException(status_code=401, detail=reason)

# 세션 대신 user_id를 딕셔너리로 반환하는 함수
def set_session(user_id: int):
    return {"user_id": user_id}

# 회원가입 처리 함수
def create_user(user_data, db: Session):
    # 닉네임 중복 확인
    if db.query(User).filter(User.nickname == user_data.nickname).first():
        raise HTTPException(status_code=400, detail="이미 사용 중인 닉네임입니다.")
     
    # 이메일 및 비밀번호 유효성 검사   
    input_email(user_data.email, db)
    input_password(user_data.password)

    # 비밀번호 확인값이 일치하는지 검사
    if user_data.password != user_data.confirm_password:
        raise HTTPException(status_code=400, detail="비밀번호가 일치하지 않습니다.")
        
    # 휴대폰 인증번호가 올바른지 검사    
    if not verify_auth_code(user_data.phone, user_data.phone_auth_code, db):
        raise HTTPException(status_code=400, detail="휴대폰 인증이 완료되지 않았습니다.")

    # 비밀번호 해싱
    hashed_pw = bcrypt.hashpw(user_data.password.encode(), bcrypt.gensalt()).decode()

    # 새 사용자 객체 생성
    new_user = User(
        name=user_data.name,
        phone=user_data.phone,
        email=user_data.email,
        password=hashed_pw,
        nickname=user_data.nickname
    )

    # DB에 사용자 추가 및 커밋
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    # user_id를 세션처럼 반환
    return set_session(new_user.id)

# 로그인 처리 함수
def authenticate_user(user: UserLogin, db: Session):
    # 이메일로 사용자 검색
    db_user = find_user_by_email(user.email, db)
    if not db_user:
        handle_login_error("존재하지 않는 이메일입니다.")
        
    # 비밀번호 일치 여부 확인   
    if not bcrypt.checkpw(user.password.encode(), db_user.password.encode()):
        handle_login_error("비밀번호가 일치하지 않습니다.")
    # 로그인 성공 시 user_id 반환    
    return set_session(db_user.id)

# 인증번호 생성 함수

def generate_auth_code(phone: str, db: Session):
    code = str(random.randint(100000, 999999)) # 6자리 랜덤 숫자 생성
    db_code = AuthModel(phone=phone, code=code) # DB 모델 인스턴스 생성
    db.add(db_code)  # DB에 저장
    db.commit()
    return code  # 생성된 인증번호 반환

# 인증번호 검증 함수
def verify_auth_code(phone: str, input_code: str, db: Session):
    # 최신 인증기록 하나 조회
    record = db.query(AuthModel.AuthCode).filter_by(phone=phone).order_by(AuthModel.AuthCode.id.desc()).first()
    # 인증번호 일치 여부 반환
    return record and record.code == input_code


"""
/services/auth_service.py
역할:
사용자 인증과 관련된 핵심 비즈니스 로직을 담당하는 서비스 레이어
회원가입, 로그인, 인증번호 생성 및 검증 등 인증 흐름 전반을 처리한다

주요 기능:
-이메일 형식 및 중복 검사
-비밀번호 유효성 검사 (특수문자 포함 8자 이상)
-이메일로 사용자 검색
-로그인 실패 시 예외 처리
-세션 역할 대체 반환 (간단히 user_id 포함 dict 반환)
-회원가입 처리 (닉네임 중복, 비밀번호 확인, 휴대폰 인증 확인 포함)
-로그인 처리 (비밀번호 검증 포함)
-인증번호 생성 및 DB 저장
-인증번호 검증 (최신 코드와 입력값 비교)

함수 목록 및 설명:
-def input_email(email, db): 이메일 형식 및 중복 확인, 오류 발생 시 HTTPException
-def input_password(password): 비밀번호 조건 검사, 미충족 시 HTTPException
-def find_user_by_email(email, db): DB에서 이메일로 사용자 조회
-def handle_login_error(reason): 로그인 실패 시 401 오류 발생
-def set_session(user_id): 세션 저장 대신 user_id 반환
-def create_user(user_data, db): 회원가입 처리, 유효성 검사 및 DB 저장 후 세션 반환
-def authenticate_user(user, db): 로그인 처리, 이메일과 비밀번호 검증 후 세션 반환
-def generate_auth_code(phone, db): 6자리 인증번호 생성 및 DB 저장 후 코드 반환
-def verify_auth_code(phone, input_code, db): DB의 최신 인증번호와 입력값 일치 여부 반환

동작 흐름 요약
회원가입 시 이메일, 비밀번호, 닉네임 중복 체크 및 휴대폰 인증 코드 검증을 거쳐 사용자 생성 후 세션 대체값 반환
로그인 시 이메일 존재 및 비밀번호 검증을 거쳐 세션 대체값 반환
인증번호 요청 시 6자리 난수 생성해 DB 저장 및 반환
인증번호 검증 시 최신 DB 저장 코드와 사용자 입력값 비교해 결과 반환
"""
