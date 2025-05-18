from fastapi import APIRouter
from ..services.mypage_service import get_user_rooms

router = APIRouter()

@router.get("/mypage/rooms/{user_id}")
def get_my_rooms(user_id: str):
    return get_user_rooms(user_id)


"""
/routers/mypage.py
역할:
마이페이지 관련 요청을 처리하는 API 라우터.
특정 사용자가 참여 중인 채팅방 목록을 조회할 수 있도록 한다.

연결된 서비스:
mypage_service.py: 사용자별 채팅방 목록 조회 로직이 구현된 서비스 레이어

엔드포인트 목록:
채팅방 목록 조회 = 메서드-GET, 경로-/mypage/rooms/{user_id}, 요청 파라미터-user_id(str), 응답-사용자의 채팅방 목록

동작 흐름 요약
/mypage/rooms/{user_id}: 사용자 ID를 받아 해당 사용자가 참여 중인 채팅방 목록을 조회하고 반환한다.
"""
