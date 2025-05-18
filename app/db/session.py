# app/db/session.py

#SQLAlchemy용 DB 연결 엔진과 세션 설정 + 제공 파일

from sqlalchemy import create_engine # DB 연결 엔진 생성용
from sqlalchemy.orm import sessionmaker, Session # 세션 생성기 및 타입 정의

DATABASE_URL = "sqlite:///./acton.db" # SQLite DB 경로

engine = create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False} # SQLite 전용 옵션
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine) # DB 세션 생성기

def get_db():
    db: Session = SessionLocal() # 세션 객체 생성
    try:
        yield db # FastAPI 의존성 주입용
    finally:
        db.close() # 사용 후 세션 닫기
