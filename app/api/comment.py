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
