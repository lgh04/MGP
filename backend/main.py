from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# ✅ 절대 경로로 모두 수정
from backend.user.routes import router as user_router
from backend.login.routes import router as login_router
from backend.law.routes import router as law_router
from backend.db.database import Base, engine  # ✅ 경로 수정

# ✅ 데이터베이스 테이블 생성
Base.metadata.create_all(bind=engine)

app = FastAPI()

# ✅ CORS 설정 (React 연결용)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # 프론트엔드 주소
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ 라우터 등록 (user_router prefix를 복수형 users로 수정)
app.include_router(user_router, prefix="/users", tags=["user"])
app.include_router(login_router, prefix="/auth", tags=["login"])
app.include_router(law_router, prefix="/api", tags=["law"])  # /api/laws 로 접근 가능
