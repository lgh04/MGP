from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# ✅ DB 연결 주소 (SQLite 기준, 나중에 PostgreSQL로 바꿔도 됨)
DATABASE_URL = "sqlite:///./acton.db"

# ✅ 엔진 생성 (SQLite에서는 connect_args 필요)
engine = create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)

# ✅ 세션 클래스 생성
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# ✅ Base 클래스 (모든 모델이 이걸 상속)
Base = declarative_base()

# ✅ FastAPI 의존성 주입용 DB 세션 생성기

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
