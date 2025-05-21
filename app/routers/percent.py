# 특정 법안에 대한 찬반 투표 결과(비율)를 계산하여 반환하는 API 라우터

from fastapi import APIRouter # FastAPI 라우터 기능 불러오기
from ..services.percent_service import calculate_vote_percentages # 투표 비율 계산을 위한 서비스 함수 가져오기
router = APIRouter() # 이 파일의 API들을 담을 라우터 인스턴스 생성

# 법안 투표 결과 비율 조회 API
@router.get("/vote/result/{law_id}") # /vote/result/<law_id> 경로로 GET 요청 시 실행
def get_vote_result(law_id: str):
     # 해당 법안 ID를 기반으로 찬반 투표 비율 계산
    result = calculate_vote_percentages(law_id)
    # 계산된 결과 반환
    return result


"""
/routers/percent.py  
역할:  
특정 법안의 투표 결과(찬성/반대 비율)를 계산하여 반환하는 API 라우터.  
사용자가 법안 ID를 통해 투표 비율 데이터를 확인할 수 있도록 한다.  

연결된 서비스:  
percent_service.py: 법안별 투표 데이터의 비율을 계산하는 로직이 구현된 서비스 레이어  

엔드포인트 목록:  
투표 결과 조회 = 메서드-GET, 경로-/vote/result/{law_id}, 요청 파라미터-law_id(str), 응답-찬성/반대 투표 비율 결과  

동작 흐름 요약  
/vote/result/{law_id}: 법안 ID를 받아 해당 법안의 투표 찬반 비율을 계산하고 결과를 반환한다.  
"""
