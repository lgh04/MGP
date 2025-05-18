#SQLAlchemy용 DB 연결 설정과 세션 관리 파일

from sqlalchemy import create_engine # DB 연결 엔진
from sqlalchemy.ext.declarative import declarative_base # 모델의 Base 클래스 생성
from sqlalchemy.orm import sessionmaker # 세션 생성기

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db" # SQLite DB 파일 경로

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False} # SQLite 전용 옵션
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine) # DB 세션 팩토리
 
Base = declarative_base() # 모델이 상속할 Base 클래스

def get_db():
    db = SessionLocal() # 세션 생성
    try:
        yield db  # 의존성 주입용
    finally:
        db.close() # 세션 종료
