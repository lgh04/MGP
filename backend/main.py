from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

# ✅ 기존 라우터들
from backend.user.routes import router as user_router
from backend.login.routes import router as login_router
from backend.law.routes import router as law_router
from backend.lawlist.routes import router as lawlist_router
from backend.lawdetail.routes import router as lawdetail_router  # ✅ 상세 라우터 추가

# ✅ 상세 API용 크루드 함수
from backend.lawdetail.crud import fetch_law_detail

# ✅ DB 설정
from backend.db.database import Base, engine
Base.metadata.create_all(bind=engine)

# ✅ 앱 생성
app = FastAPI()

# ✅ CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ 라우터 등록
app.include_router(user_router, prefix="/users", tags=["user"])
app.include_router(login_router, prefix="/auth", tags=["login"])
app.include_router(law_router, prefix="/api", tags=["law"])
app.include_router(lawlist_router, prefix="/api", tags=["lawlist"])
app.include_router(lawdetail_router, prefix="/api", tags=["lawdetail"])  # ⬅ 상세 라우터까지 등록함

# ✅ 상세 단건 조회용 직접 라우트 (추가로 필요한 경우 사용)
@app.get("/api/law/{bill_id}")
def get_law(bill_id: str):
    try:
        data = fetch_law_detail(bill_id)
        if not data:
            raise HTTPException(status_code=404, detail="해당 법안을 찾을 수 없습니다.")
        return JSONResponse(content=data)
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)
