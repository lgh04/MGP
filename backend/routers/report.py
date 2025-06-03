from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from typing import List

from database import get_db
from models.report import Report, UserReportStatus
from models.user import User
from models.message import Message

router = APIRouter()

REPORT_THRESHOLD = 3  # 신고 제한 횟수
RESTRICTION_HOURS = 24  # 제한 시간 (시간 단위)

@router.post("/messages/{message_id}/report")
async def report_message(
    message_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # 메시지 존재 여부 확인
    message = db.query(Message).filter(Message.id == message_id).first()
    if not message:
        raise HTTPException(status_code=404, detail="Message not found")

    # 자기 자신을 신고하는지 확인
    if message.user_id == current_user.id:
        raise HTTPException(status_code=400, detail="Cannot report your own message")

    # 이미 신고한 메시지인지 확인
    existing_report = db.query(Report).filter(
        Report.message_id == message_id,
        Report.reporter_id == current_user.id
    ).first()
    if existing_report:
        raise HTTPException(status_code=400, detail="Already reported this message")

    # 신고 기록 생성
    report = Report(
        reported_user_id=message.user_id,
        reporter_id=current_user.id,
        message_id=message_id,
        discussion_id=message.discussion_id
    )
    db.add(report)

    # 사용자의 신고 상태 조회 또는 생성
    report_status = db.query(UserReportStatus).filter(
        UserReportStatus.user_id == message.user_id,
        UserReportStatus.discussion_id == message.discussion_id
    ).first()

    if not report_status:
        report_status = UserReportStatus(
            user_id=message.user_id,
            discussion_id=message.discussion_id
        )
        db.add(report_status)

    # 신고 횟수 증가
    report_status.report_count += 1

    # 신고 횟수가 임계값을 넘으면 제한 설정
    if report_status.report_count >= REPORT_THRESHOLD:
        report_status.is_restricted = True
        report_status.restriction_start = datetime.utcnow()
        report_status.restriction_end = datetime.utcnow() + timedelta(hours=RESTRICTION_HOURS)

    db.commit()
    return {"status": "success", "message": "Report submitted successfully"}

@router.get("/users/{user_id}/report-status/{discussion_id}")
async def get_user_report_status(
    user_id: int,
    discussion_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    status = db.query(UserReportStatus).filter(
        UserReportStatus.user_id == user_id,
        UserReportStatus.discussion_id == discussion_id
    ).first()

    if not status:
        return {
            "report_count": 0,
            "is_restricted": False,
            "restriction_end": None
        }

    # 제한 시간이 지났는지 확인
    if status.is_restricted and status.restriction_end and status.restriction_end < datetime.utcnow():
        status.is_restricted = False
        status.restriction_start = None
        status.restriction_end = None
        status.report_count = 0
        db.commit()

    return {
        "report_count": status.report_count,
        "is_restricted": status.is_restricted,
        "restriction_end": status.restriction_end
    } 