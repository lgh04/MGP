from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "sqlite:///./acton.db" # SQLite 경로

engine = create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False} # SQLite 전용 옵션
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)  # 세션 생성기

Base = declarative_base() # 모든 모델이 상속할 Base 클래스

def get_db():
    db = SessionLocal() # DB 세션 시작
    try:
        yield db # FastAPI 의존성 주입용
    finally:
        db.close() # 세션 종료
