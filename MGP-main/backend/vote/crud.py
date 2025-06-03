from sqlalchemy.orm import Session
from sqlalchemy import func
from backend.db.models import Vote
from backend.db.database import SessionLocal

def get_vote_count(db: Session, bill_id: str):
    """특정 법안의 투표 현황을 조회합니다."""
    agree_count = db.query(func.count(Vote.id)).filter(
        Vote.bill_id == bill_id,
        Vote.vote_type == 'agree'
    ).scalar()

    disagree_count = db.query(func.count(Vote.id)).filter(
        Vote.bill_id == bill_id,
        Vote.vote_type == 'disagree'
    ).scalar()

    total_count = agree_count + disagree_count
    
    if total_count == 0:
        return {
            "agree_count": 0,
            "disagree_count": 0,
            "agree_percent": 0,
            "disagree_percent": 0,
            "total_count": 0
        }

    return {
        "agree_count": agree_count,
        "disagree_count": disagree_count,
        "agree_percent": round((agree_count / total_count) * 100, 1),
        "disagree_percent": round((disagree_count / total_count) * 100, 1),
        "total_count": total_count
    }

def get_user_vote(db: Session, bill_id: str, user_id: int):
    """사용자의 특정 법안에 대한 투표를 조회합니다."""
    return db.query(Vote).filter(
        Vote.bill_id == bill_id,
        Vote.user_id == user_id
    ).first()

def create_or_update_vote(db: Session, bill_id: str, user_id: int, vote_type: str):
    """투표를 생성하거나 업데이트합니다."""
    existing_vote = get_user_vote(db, bill_id, user_id)
    
    if existing_vote:
        existing_vote.vote_type = vote_type
        db.commit()
        db.refresh(existing_vote)
        return existing_vote
    
    new_vote = Vote(
        bill_id=bill_id,
        user_id=user_id,
        vote_type=vote_type
    )
    db.add(new_vote)
    db.commit()
    db.refresh(new_vote)
    return new_vote 