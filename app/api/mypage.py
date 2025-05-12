from fastapi import APIRouter
from ..services.mypage_service import get_user_rooms

router = APIRouter()

@router.get("/mypage/rooms/{user_id}")
def get_my_rooms(user_id: str):
    return get_user_rooms(user_id)
