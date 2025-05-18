# 법안에 대한 댓글을 등록하는 API 라우터

from fastapi import APIRouter # 라우터 생성용
from pydantic import BaseModel # 요청 데이터 검증용 모델
from ..services.comment_service import submit_comment # 댓글 등록 로직 함수

router = APIRouter() # 라우터 인스턴스 생성

# 요청 본문 형식 정의
class CommentRequest(BaseModel):
    user_id: str # 작성자 ID
    law_id: str # 대상 법안 ID
    content: str # 댓글 내용

# 댓글 등록 API (POST /comment)
@router.post("/comment")
def add_comment(comment: CommentRequest):
    success = submit_comment(comment.user_id, comment.law_id, comment.content) # 댓글 저장 처리
    return {"success": success} # 성공 여부 반환
