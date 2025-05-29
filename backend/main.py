from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

# 기존 라우터들
from backend.user.routes import router as user_router
from backend.login.routes import router as login_router
from backend.law.routes import router as law_router
from backend.lawlist.routes import router as lawlist_router
from backend.lawdetail.routes import router as lawdetail_router

# 새로 만든 크루드 함수 import
from backend.lawdetail.crud import fetch_law_by_bill_no

# DB 설정
from backend.db.database import Base, engine
Base.metadata.create_all(bind=engine)

# 앱 생성
app = FastAPI()

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 기존 라우터 등록
app.include_router(user_router, prefix="/users", tags=["user"])
app.include_router(login_router, prefix="/auth", tags=["login"])
app.include_router(law_router, prefix="/api", tags=["law"])
app.include_router(lawlist_router, prefix="/api", tags=["lawlist"])
app.include_router(lawdetail_router, prefix="/api", tags=["lawdetail"])

# ✅ 새로 추가된 단일 법안 조회 엔드포인트
@app.get("/api/law/{bill_no}")
def get_law(bill_no: str):
    try:
        data = fetch_law_by_bill_no(bill_no)
        return JSONResponse(content=data)
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)
