# 법안에 대한 투표 결과를 백분율로 계산해주는 라우터

from fastapi import APIRouter # 라우터 생성용
from ..services.percent_service import calculate_vote_percentages # 찬반 비율 계산 서비스 함수

router = APIRouter() # 라우터 인스턴스 생성

# 특정 법안 ID에 대한 투표 결과를 백분율로 계산하여 반환
@router.get("/vote/result/{law_id}")
def get_vote_result(law_id: str):
    result = calculate_vote_percentages(law_id) # law_id를 기반으로 찬반 비율 계산
    return result # {"yes": 60.0, "no": 40.0} 등 비율 반환
