from fastapi import APIRouter
from pydantic import BaseModel
from ..services.chat_service import send_message, get_chat_history

router = APIRouter()

class MessageRequest(BaseModel):
    user_id: str
    room_id: str
    message: str

@router.post("/chat/send")
def send_chat(msg: MessageRequest):
    success = send_message(msg.user_id, msg.room_id, msg.message)
    return {"success": success}

@router.get("/chat/{room_id}")
def fetch_chat(room_id: str):
    return get_chat_history(room_id)



"""
/routers/chat.py
역할:
채팅 관련 요청을 처리하는 API 라우터.
사용자가 메시지를 전송하거나 특정 채팅방의 대화 기록을 불러오는 기능을 담당한다.

연결된 서비스:
chat_service.py: 메시지 저장 및 채팅 기록 조회 로직이 구현된 서비스 레이어
pydantic.BaseModel: 메시지 전송 요청 데이터 구조 정의

엔드포인트 목록:
채팅 전송 = 메서드-POST, 경로-/chat/send, 요청 스키마-MessageRequest, 응답-성공 여부 (success: bool)
채팅 조회 = 메서드-GET, 경로-/chat/{room_id}, 요청 파라미터-room_id(str), 응답-해당 채팅방의 메시지 목록

동작 흐름 요약
/chat/send: 사용자 ID, 채팅방 ID, 메시지를 받아 해당 방에 메시지를 저장하고 성공 여부를 반환한다.
/chat/{room_id}: 채팅방 ID를 입력받아 해당 채팅방의 전체 메시지 기록을 조회하고 반환한다.
"""
