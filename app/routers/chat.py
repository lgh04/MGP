# 특정 채팅방에 메시지를 보내고, 해당 채팅방의 전체 채팅 기록을 조회하는 API 라우터

from fastapi import APIRouter # FastAPI의 라우터 기능을 가져옴
from pydantic import BaseModel # 요청 데이터 검증을 위한 Pydantic의 BaseModel 사용
from ..services.chat_service import send_message, get_chat_history # 채팅 관련 서비스 함수 (메시지 전송, 기록 조회) 불러오기

router = APIRouter() # 이 라우터에 포함될 API 경로들을 정의할 라우터 인스턴스 생성

# 메시지 전송 요청을 위한 데이터 모델 정의
class MessageRequest(BaseModel):
    user_id: str # 메시지를 보내는 사용자 ID
    room_id: str # 메시지를 보낼 채팅방 ID
    message: str # 전송할 메시지 본문

# 메시지 전송 API
@router.post("/chat/send") # POST 요청으로 /chat/send 경로 호출 시 실행됨
def send_chat(msg: MessageRequest ):
    # 메시지 전송 서비스 함수 호출 (user_id, room_id, message 전달)
    success = send_message(msg.user_id, msg.room_id, msg.message)
    # 전송 성공 여부를 JSON 형태로 응답
    return {"success": success}

# 채팅 기록 조회 API
@router.get("/chat/{room_id}") # GET 요청으로 /chat/<room_id> 호출 시 실행됨
def fetch_chat(room_id: str):
     # 해당 채팅방의 기록을 불러와 반환
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
