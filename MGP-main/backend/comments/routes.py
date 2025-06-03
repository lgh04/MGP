from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from backend.db.database import get_db
from backend.db.models import Comment, User
from backend.user.auth import get_current_user
from pydantic import BaseModel
from typing import List
from datetime import datetime

router = APIRouter(
    prefix="/api",
    tags=["comments"]
)

class CommentCreate(BaseModel):
    content: str

class CommentResponse(BaseModel):
    id: int
    content: str
    created_at: datetime
    user_nickname: str

    class Config:
        from_attributes = True

@router.get("/comments/{bill_id}", response_model=List[CommentResponse])
async def get_comments(bill_id: str, db: Session = Depends(get_db)):
    """특정 법안의 댓글 목록을 조회합니다."""
    comments = db.query(Comment).filter(Comment.bill_id == bill_id).all()
    
    # 댓글과 사용자 정보를 결합
    result = []
    for comment in comments:
        user = db.query(User).filter(User.id == comment.user_id).first()
        result.append({
            "id": comment.id,
            "content": comment.content,
            "created_at": comment.created_at,
            "user_nickname": user.nickname if user else "알 수 없음"
        })
    
    return result

@router.post("/comments/{bill_id}", response_model=CommentResponse)
async def create_comment(
    bill_id: str,
    comment: CommentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """새로운 댓글을 작성합니다."""
    db_comment = Comment(
        bill_id=bill_id,
        user_id=current_user.id,
        content=comment.content
    )
    db.add(db_comment)
    db.commit()
    db.refresh(db_comment)
    
    return {
        "id": db_comment.id,
        "content": db_comment.content,
        "created_at": db_comment.created_at,
        "user_nickname": current_user.nickname
    }

@router.delete("/comments/{comment_id}")
async def delete_comment(
    comment_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """댓글을 삭제합니다."""
    comment = db.query(Comment).filter(Comment.id == comment_id).first()
    if not comment:
        raise HTTPException(status_code=404, detail="댓글을 찾을 수 없습니다.")
    
    if comment.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="자신의 댓글만 삭제할 수 있습니다.")
    
    db.delete(comment)
    db.commit()
    return {"message": "댓글이 삭제되었습니다."}
