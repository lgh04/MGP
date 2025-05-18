#법안 상세 정보 조회 API 라우터

from fastapi import APIRouter # 라우터 생성용
from app.services.law_service import fetch_law_detail # 법안 상세 조회 서비스 함수

router = APIRouter() # 라우터 인스턴스 생성

# 법안 상세 조회 API (GET /law/{law_id})
@router.get("/law/{law_id}")
def get_law_detail(law_id: str):
    return fetch_law_detail(law_id) # 서비스 함수에 law_id 전달해 조회 결과 반환
