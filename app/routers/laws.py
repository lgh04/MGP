from fastapi import APIRouter
from app.services.law_service import fetch_law_detail

router = APIRouter()

@router.get("/law/{law_id}")
def get_law_detail(law_id: str):
    return fetch_law_detail(law_id)


"""
/routers/laws.py
역할:
특정 법안의 상세 정보를 조회하는 API 라우터.
사용자가 법안의 ID를 통해 해당 법안의 상세 내용을 확인할 수 있도록 한다.

연결된 서비스:
law_service.py: 법안 상세 정보 조회 로직이 구현된 서비스 레이어

엔드포인트 목록:
법안 상세 조회 = 메서드-GET, 경로-/law/{law_id}, 요청 파라미터-law_id(str), 응답-해당 법안의 상세 정보

동작 흐름 요약
/law/{law_id}: 법안 ID를 받아 해당 법안의 상세 정보를 조회하고 반환한다.
"""
