# 사용자가 참여 중인 토론방 목록을 조회하는 API 라우터

from fastapi import APIRouter # FastAPI 라우터 생성용
from ..services.mypage_service import get_user_rooms # 유저별 방 조회 서비스 함수

# 특정 사용자 ID로 사용자가 참여 중인 토론방 목록을 조회하는 API
router = APIRouter() # 라우터 인스턴스 생성

@router.get("/mypage/rooms/{user_id}")
def get_my_rooms(user_id: str):
    return get_user_rooms(user_id) # user_id를 기반으로 토론방 리스트 반환
