import os
from sqlalchemy import create_engine, inspect
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session

# 프로젝트 루트 디렉토리 경로 계산
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# SQLite DB 경로 지정
SQLALCHEMY_DATABASE_URL = f"sqlite:///{os.path.join(BASE_DIR, 'sql_app.db')}"

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db: Session = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# 데이터베이스 테이블 생성 (테이블이 없을 때만)
def create_tables():
    from . import models  # 모델 import
    inspector = inspect(engine)
    
    # users 테이블이 없을 때만 테이블 생성
    if not inspector.has_table("users"):
        Base.metadata.create_all(bind=engine)
        print("Tables created successfully")
    else:
        print("Tables already exist")

# 테이블 생성 실행
create_tables()
