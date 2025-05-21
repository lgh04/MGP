# 특정 법안에 대한 사용자의 댓글을 등록하는 API 라우터

from fastapi import APIRouter # FastAPI의 라우터 기능을 가져옴
from pydantic import BaseModel # 요청 데이터 구조를 정의하기 위한 Pydantic 모델
from ..services.comment_service import submit_comment # 댓글 등록 관련 서비스 함수 불러오기

# 이 파일에서 정의한 API들을 포함할 라우터 인스턴스 생성
router = APIRouter()

# 댓글 등록 요청을 위한 데이터 모델 정의
class CommentRequest(BaseModel):
    user_id: str # 댓글을 작성한 사용자 ID
    law_id: str # 댓글이 달릴 대상 법안 ID
    content: str # 댓글 내용

# 댓글 등록 API
@router.post("/comment") # POST 요청으로 /comment 경로 호출 시 실행됨
def add_comment(comment: CommentRequest):
     # 서비스 함수에 user_id, law_id, content를 넘겨 댓글 등록 처리
    success = submit_comment(comment.user_id, comment.law_id, comment.content)
     # 등록 성공 여부를 JSON 형태로 반환
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
