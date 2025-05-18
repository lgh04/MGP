# FastAPI 앱의 진입점으로, 모든 라우터와 설정을 통합하고 앱을 실행하는 메인 파일

from fastapi import FastAPI # FastAPI 인스턴스 생성을 위한 모듈
from .routers import auth, laws, chat, comment, mypage, percent, vote, votecheck, search, summary # 라우터 모듈들
from app.routers import search
from app.scheduler import start_scheduler # 스케줄러 실행 함수
from app.tasks.scheduler import start_scheduler
from app.db import engine, Base # DB 엔진과 모델 베이스 클래스

app = FastAPI() # FastAPI 앱 인스턴스 생성

# 라우터 등록 (API 기능별 경로 연결)
app.include_router(auth.router) # 회원가입, 로그인 등 인증 기능
app.include_router(laws.router)  # 법안 상세 조회 등
app.include_router(search.router, prefix="/bills", tags=["bills"]) # 법안 검색
app.include_router(summary.router, prefix="/bills", tags=["summary"]) # 법안 요약
app.include_router(chat.router) # 채팅 기능
app.include_router(comment.router) # 댓글 기능
app.include_router(mypage.router) # 마이페이지 관련 API
app.include_router(percent.router) # 찬반 비율 계산
app.include_router(vote.router) # 투표 제출
app.include_router(votecheck.router) # 투표 여부 확인
app.include_router(search.router) 

# 라우터 등록
#app.include_router(auth.router, prefix="/auth")


# DB 테이블 생성
Base.metadata.create_all(bind=engine)

# 스케줄러 시작 (예: 자동 작업 실행)
start_scheduler() # app.scheduler와 app.tasks.scheduler 중 하나만 선택 필요

# 루트 엔드포인트 (테스트용)
@app.get("/")
def read_root():
    return {"message": "Welcome to the ACT:ON API"} # 기본 메시지 반환
