from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

# ✅ 기존 라우터들
from backend.user.routes import router as user_router
from backend.login.routes import router as login_router
from backend.law.routes import router as law_router
from backend.lawlist.routes import router as lawlist_router
from backend.lawdetail.routes import router as lawdetail_router
from backend.vote.routes import router as vote_router
from backend.comments.routes import router as comments_router

# ✅ 상세 API용 크루드 함수
from backend.lawdetail.crud import fetch_law_detail

# ✅ DB 설정
from backend.db.database import Base, engine, create_tables

# ✅ 앱 생성
app = FastAPI()

# ✅ CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:3001"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*", "Authorization", "Content-Type"],
    expose_headers=["*"]
)

# ✅ 데이터베이스 테이블 생성
create_tables()

# ✅ 라우터 등록
app.include_router(user_router, prefix="/api", tags=["users"])
app.include_router(login_router)  # prefix 제거 (이미 라우터에서 /api 포함)
app.include_router(law_router, prefix="/api", tags=["law"])
app.include_router(lawlist_router, prefix="/api", tags=["lawlist"])
app.include_router(lawdetail_router, prefix="/api", tags=["lawdetail"])
app.include_router(vote_router)  # prefix 제거 (이미 라우터에서 /api 포함)
app.include_router(comments_router)  # prefix 제거 (이미 라우터에서 /api 포함)

# ✅ 상세 단건 조회용 직접 라우트
@app.get("/api/law/{bill_id}")
async def get_law(bill_id: str):
    try:
        if not bill_id or bill_id == "undefined":
            return JSONResponse(
                status_code=400,
                content={"error": "유효하지 않은 법안 ID입니다."}
            )
            
        data = fetch_law_detail(bill_id)
        
        if isinstance(data, dict) and "error" in data:
            return JSONResponse(
                status_code=404,
                content=data
            )
            
        return JSONResponse(content=data)
        
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"error": "내부 서버 오류가 발생했습니다.", "detail": str(e)}
        )


@app.get("/")
def read_root():
    return {"message": "✅ FastAPI 서버가 정상 작동 중입니다!"}

