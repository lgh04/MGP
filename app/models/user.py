#사용자(User)정보와 휴대폰 인증 코드(AuthCode)를 저장하는 데이터베이스 테이블을 정의한 모델 코드

from sqlalchemy import Column, Integer, String, DateTime, func
from app.db import Base # SQLAlchemy의 모델 기반 클래스

# 인증번호 저장 테이블: 전화번호로 전송된 인증 코드 정보 저장
class AuthCode(Base):
    __tablename__ = "auth_codes" # 테이블 이름: auth_codes

    id = Column(Integer, primary_key=True, index=True) # 고유 ID (자동 증가)
    phone = Column(String, nullable=False) # 전화번호 (빈 값 불가)
    code = Column(String, nullable=False) # 전송된 인증번호 (빈 값 불가)
    created_at = Column(DateTime(timezone=True), server_default=func.now()) # 생성 시간 (자동 저장)

# 사용자 정보 저장 테이블
class User(Base):
    __tablename__ = "users" # 테이블 이름: users

    id = Column(Integer, primary_key=True, autoincrement=True) # 고유 ID (자동 증가)
    name = Column(String) # 사용자 이름
    phone = Column(String, unique=True, index=True) # 전화번호 (중복 불가, 검색용 인덱스 생성)
    email = Column(String, unique=True, index=True) # 이메일 (중복 불가, 검색용 인덱스 생성)
    password = Column(String) # 비밀번호 (해싱된 값 저장됨)
    nickname = Column(String, unique=True, index=True) # 닉네임 (중복 불가, 검색용 인덱스 생성)

