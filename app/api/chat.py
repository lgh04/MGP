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
