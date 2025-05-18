#채팅 메시지 전송과 조회 기능 처리 API 라우터

from fastapi import APIRouter # 라우터 생성용
from pydantic import BaseModel # 요청 데이터 검증용 모델
from ..services.chat_service import send_message, get_chat_history # 채팅 처리 로직

router = APIRouter() # 라우터 인스턴스 생성

# 요청 바디에 사용할 데이터 모델 정의
class MessageRequest(BaseModel):
    user_id: str # 사용자 ID
    room_id: str # 채팅방 ID
    message: str # 보낼 메시지 내용
    
# 메시지 전송 API (POST /chat/send)
@router.post("/chat/send")
def send_chat(msg: MessageRequest):
    success = send_message(msg.user_id, msg.room_id, msg.message) # 메시지를 DB에 저장
    return {"success": success} # 성공 여부 반환

# 채팅 내역 조회 API (GET /chat/{room_id})
@router.get("/chat/{room_id}")
def fetch_chat(room_id: str):
    return get_chat_history(room_id) # 해당 방의 채팅 메시지 목록 반환
