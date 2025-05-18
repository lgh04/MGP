from fastapi import APIRouter
from pydantic import BaseModel
from ..services.comment_service import submit_comment

router = APIRouter()

class CommentRequest(BaseModel):
    user_id: str
    law_id: str
    content: str

@router.post("/comment")
def add_comment(comment: CommentRequest):
    success = submit_comment(comment.user_id, comment.law_id, comment.content)
    return {"success": success}



"""
/routers/comment.py
역할:
법안에 대한 댓글 작성 요청을 처리하는 API 라우터.
사용자가 특정 법안에 댓글을 등록할 수 있도록 한다.

연결된 서비스:
comment_service.py: 댓글 저장 로직이 구현된 서비스 레이어
pydantic.BaseModel: 댓글 요청 데이터 구조 정의

엔드포인트 목록:
댓글 등록 = 메서드-POST, 경로-/comment, 요청 스키마-CommentRequest, 응답-성공 여부 (success: bool)

동작 흐름 요약
/comment: 사용자 ID, 법안 ID, 댓글 내용을 받아 해당 법안에 댓글을 등록하고 성공 여부를 반환한다.
"""
