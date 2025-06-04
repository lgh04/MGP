from fastapi import APIRouter, Depends, HTTPException, WebSocket, WebSocketDisconnect, status
from sqlalchemy.orm import Session
from sqlalchemy import desc, create_engine, text
from typing import List
from backend.db.database import get_db, engine
from backend.user.auth import get_current_user
from .models import Discussion, DiscussionParticipant, DiscussionMessage, UserChatRestriction
from . import schemas
from datetime import datetime, timedelta
from backend.db.models import User
import httpx
import json
from jose import jwt
from backend.user.auth import SECRET_KEY, ALGORITHM

router = APIRouter(prefix="/api/discussions", tags=["discussions"])

# WebSocket 연결을 저장할 딕셔너리
connected_clients = {}

# user_chat_restrictions 테이블 생성 함수
def create_user_chat_restrictions_table():
    """user_chat_restrictions 테이블을 생성합니다."""
    with engine.connect() as conn:
        # 테이블이 이미 존재하는지 확인
        result = conn.execute(text("""
            SELECT name FROM sqlite_master 
            WHERE type='table' AND name='user_chat_restrictions'
        """))
        exists = result.scalar() is not None

        if not exists:
            conn.execute(text("""
                CREATE TABLE user_chat_restrictions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER REFERENCES users(id),
                    discussion_id INTEGER REFERENCES discussions(id),
                    restricted_until TIMESTAMP,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """))
            conn.commit()
            print("user_chat_restrictions 테이블 생성됨")
        
        # 만료된 제한 삭제
        conn.execute(text("""
            DELETE FROM user_chat_restrictions 
            WHERE restricted_until < datetime('now')
        """))
        conn.commit()

# 테이블 생성 실행
create_user_chat_restrictions_table()

async def get_bill_name(bill_id: str) -> str:
    """법안 API에서 법안 제목을 가져옵니다."""
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"${process.env.NEXT_PUBLIC_API_URL}/api/law/{bill_id}")
            if response.status_code == 200:
                data = response.json()
                return data.get("BILL_NAME", "알 수 없는 법안")
            return "알 수 없는 법안"
    except Exception as e:
        print(f"법안 정보 조회 실패: {e}")
        return "알 수 없는 법안"

async def get_user_from_token(token: str, db: Session):
    """토큰에서 사용자 정보를 가져옵니다."""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            return None
        
        user = db.query(User).filter(User.email == email).first()
        return user
    except Exception as e:
        print(f"Token decode error: {e}")
        return None

@router.post("/{bill_id}/join", response_model=schemas.Discussion)
async def join_discussion(
    bill_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # 토론방 찾기 또는 생성
    discussion = db.query(Discussion).filter(
        Discussion.bill_id == bill_id
    ).first()
    
    if not discussion:
        # 새로운 토론방 생성
        discussion = Discussion(bill_id=bill_id)
        db.add(discussion)
        db.commit()
        db.refresh(discussion)
        
        # 신고 테이블 생성
        discussion.create_report_table()
    
    # 이미 참여 중인지 확인
    existing_participant = db.query(DiscussionParticipant).filter(
        DiscussionParticipant.discussion_id == discussion.id,
        DiscussionParticipant.user_id == current_user.id
    ).first()
    
    if not existing_participant:
        participant = DiscussionParticipant(
            discussion_id=discussion.id,
            user_id=current_user.id
        )
        db.add(participant)
        db.commit()
    
    return {
        "id": discussion.id,
        "bill_id": discussion.bill_id,
        "created_at": discussion.created_at,
        "participant_count": db.query(DiscussionParticipant).filter(
            DiscussionParticipant.discussion_id == discussion.id
        ).count(),
        "is_participating": True
    }

@router.delete("/{bill_id}/leave")
async def leave_discussion(
    bill_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    discussion = db.query(Discussion).filter(
        Discussion.bill_id == bill_id
    ).first()
    
    if not discussion:
        raise HTTPException(status_code=404, detail="토론방을 찾을 수 없습니다")
    
    participant = db.query(DiscussionParticipant).filter(
        DiscussionParticipant.discussion_id == discussion.id,
        DiscussionParticipant.user_id == current_user.id
    ).first()
    
    if not participant:
        raise HTTPException(status_code=404, detail="참여 중인 토론방이 아닙니다")
    
    db.delete(participant)
    db.commit()
    
    return {"message": "토론방에서 나갔습니다"}

@router.get("/", response_model=List[schemas.DiscussionListItem])
async def get_discussions(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    discussions = db.query(Discussion).order_by(desc(Discussion.created_at)).all()
    
    result = []
    for discussion in discussions:
        bill_name = await get_bill_name(discussion.bill_id)
        result.append({
            "id": discussion.id,
            "bill_id": discussion.bill_id,
            "bill_name": bill_name,
            "participant_count": db.query(DiscussionParticipant).filter(
                DiscussionParticipant.discussion_id == discussion.id
            ).count(),
            "is_participating": db.query(DiscussionParticipant).filter(
                DiscussionParticipant.discussion_id == discussion.id,
                DiscussionParticipant.user_id == current_user.id
            ).first() is not None
        })
    return result

@router.get("/my", response_model=List[schemas.MyDiscussion])
async def get_my_discussions(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    participants = db.query(DiscussionParticipant).filter(
        DiscussionParticipant.user_id == current_user.id
    ).all()
    
    discussions = []
    for participant in participants:
        discussion = participant.discussion
        last_message = db.query(DiscussionMessage).filter(
            DiscussionMessage.discussion_id == discussion.id
        ).order_by(desc(DiscussionMessage.created_at)).first()
        
        # 법안 제목 가져오기
        bill_name = await get_bill_name(discussion.bill_id)
        
        discussions.append({
            "id": discussion.id,
            "bill_id": discussion.bill_id,
            "bill_name": bill_name,
            "participant_count": db.query(DiscussionParticipant).filter(
                DiscussionParticipant.discussion_id == discussion.id
            ).count(),
            "last_message": last_message.content if last_message else None,
            "last_message_time": last_message.created_at if last_message else None
        })
    
    return discussions

@router.get("/{discussion_id}/messages", response_model=List[schemas.Message])
async def get_messages(
    discussion_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # 참여 중인지 확인
    participant = db.query(DiscussionParticipant).filter(
        DiscussionParticipant.discussion_id == discussion_id,
        DiscussionParticipant.user_id == current_user.id
    ).first()
    
    if not participant:
        raise HTTPException(status_code=403, detail="참여하지 않은 토론방입니다")
    
    messages = db.query(DiscussionMessage).filter(
        DiscussionMessage.discussion_id == discussion_id
    ).order_by(DiscussionMessage.created_at).all()
    
    return [{
        "id": msg.id,
        "content": msg.content,
        "user_id": msg.user_id,
        "user_nickname": msg.user.nickname if msg.user else "알 수 없음",
        "created_at": msg.created_at,
        "discussion_id": msg.discussion_id
    } for msg in messages]

def is_user_restricted(db: Session, user_id: int, discussion_id: int) -> bool:
    """사용자가 현재 채팅 제한 상태인지 확인합니다."""
    with engine.connect() as conn:
        result = conn.execute(text("""
            SELECT * FROM user_chat_restrictions 
            WHERE user_id = :user_id AND discussion_id = :discussion_id 
            AND restricted_until > datetime('now')
        """), {"user_id": user_id, "discussion_id": discussion_id})
        return result.fetchone() is not None

@router.post("/{discussion_id}/messages", response_model=schemas.Message)
async def create_message(
    discussion_id: int,
    message: schemas.MessageCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # 참여 중인지 확인
    participant = db.query(DiscussionParticipant).filter(
        DiscussionParticipant.discussion_id == discussion_id,
        DiscussionParticipant.user_id == current_user.id
    ).first()
    
    if not participant:
        raise HTTPException(status_code=403, detail="참여하지 않은 토론방입니다")
    
    # 채팅 제한 상태 확인
    if is_user_restricted(db, current_user.id, discussion_id):
        raise HTTPException(
            status_code=403,
            detail="신고로 인해 24시간 동안 채팅이 제한되었습니다"
        )
    
    db_message = DiscussionMessage(
        discussion_id=discussion_id,
        user_id=current_user.id,
        content=message.content
    )
    db.add(db_message)
    db.commit()
    db.refresh(db_message)
    
    return {
        "id": db_message.id,
        "content": db_message.content,
        "user_id": db_message.user_id,
        "user_nickname": current_user.nickname,
        "created_at": db_message.created_at,
        "discussion_id": db_message.discussion_id
    }

@router.websocket("/{discussion_id}/ws")
async def websocket_endpoint(
    websocket: WebSocket,
    discussion_id: int,
    token: str,
    db: Session = Depends(get_db)
):
    await websocket.accept()
    
    try:
        # 토큰 검증 및 사용자 정보 가져오기
        current_user = await get_user_from_token(token, db)
        if not current_user:
            await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
            return

        # 참여 중인지 확인
        participant = db.query(DiscussionParticipant).filter(
            DiscussionParticipant.discussion_id == discussion_id,
            DiscussionParticipant.user_id == current_user.id
        ).first()
        
        if not participant:
            await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
            return
        
        # 연결 저장
        if discussion_id not in connected_clients:
            connected_clients[discussion_id] = []
        connected_clients[discussion_id].append(websocket)
        
        try:
            while True:
                data = await websocket.receive_text()
                
                # 채팅 제한 상태 재확인
                if is_user_restricted(db, current_user.id, discussion_id):
                    await websocket.send_json({"error": "채팅이 제한되었습니다."})
                    continue
                
                # 메시지 저장
                message = DiscussionMessage(
                    discussion_id=discussion_id,
                    user_id=current_user.id,
                    content=data
                )
                db.add(message)
                db.commit()
                db.refresh(message)
                
                # 모든 연결된 클라이언트에게 메시지 전송
                message_data = {
                    "id": message.id,
                    "content": message.content,
                    "user_id": message.user_id,
                    "user_nickname": current_user.nickname,
                    "created_at": message.created_at.isoformat(),
                    "discussion_id": message.discussion_id
                }
                
                for client in connected_clients[discussion_id]:
                    try:
                        await client.send_json(message_data)
                    except Exception as e:
                        print(f"메시지 전송 실패: {e}")
                        continue
                
        except WebSocketDisconnect:
            if discussion_id in connected_clients and websocket in connected_clients[discussion_id]:
                connected_clients[discussion_id].remove(websocket)
                if not connected_clients[discussion_id]:
                    del connected_clients[discussion_id]
    
    except Exception as e:
        print(f"WebSocket error: {e}")
        if discussion_id in connected_clients and websocket in connected_clients[discussion_id]:
            connected_clients[discussion_id].remove(websocket)
            if not connected_clients[discussion_id]:
                del connected_clients[discussion_id]
        await websocket.close(code=status.WS_1011_INTERNAL_ERROR)

@router.post("/{discussion_id}/report", response_model=schemas.Report)
async def report_user(
    discussion_id: int,
    report: schemas.ReportCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # 1. 토론방이 존재하는지 확인
    discussion = db.query(Discussion).filter(Discussion.id == discussion_id).first()
    if not discussion:
        raise HTTPException(status_code=404, detail="토론방을 찾을 수 없습니다")

    # 2. 신고하려는 메시지가 해당 토론방의 메시지인지 확인
    message = db.query(DiscussionMessage).filter(
        DiscussionMessage.id == report.message_id,
        DiscussionMessage.discussion_id == discussion_id
    ).first()
    if not message:
        raise HTTPException(status_code=404, detail="메시지를 찾을 수 없습니다")

    # 3. 자기 자신을 신고하는지 확인
    if current_user.id == report.reported_user_id:
        raise HTTPException(status_code=400, detail="자기 자신을 신고할 수 없습니다")

    # 4. 이미 신고했는지 확인
    table_name = f"discussion_{discussion_id}_reports"
    with engine.connect() as conn:
        check_query = text(f"""
            SELECT id FROM {table_name}
            WHERE reporter_id = :reporter_id AND reported_user_id = :reported_user_id
        """)
        
        result = conn.execute(
            check_query,
            {
                "reporter_id": current_user.id,
                "reported_user_id": report.reported_user_id
            }
        ).first()

        if result:
            raise HTTPException(status_code=400, detail="이미 신고한 사용자입니다")

        # 5. 신고 정보 저장
        insert_query = text(f"""
            INSERT INTO {table_name} (reporter_id, reported_user_id, message_id, created_at)
            VALUES (:reporter_id, :reported_user_id, :message_id, :created_at)
        """)

        conn.execute(
            insert_query,
            {
                "reporter_id": current_user.id,
                "reported_user_id": report.reported_user_id,
                "message_id": report.message_id,
                "created_at": datetime.now()
            }
        )
        conn.commit()

        # 6. 신고 횟수 확인
        count_query = text(f"""
            SELECT COUNT(*) as report_count 
            FROM {table_name} 
            WHERE reported_user_id = :user_id
        """)
        count_result = conn.execute(count_query, {"user_id": report.reported_user_id})
        report_count = count_result.scalar()

        # 7. 3번 이상 신고당했으면 24시간 제한
        if report_count >= 3:
            # 이미 제한이 있는지 확인
            restriction_check = conn.execute(text("""
                SELECT * FROM user_chat_restrictions 
                WHERE user_id = :user_id AND discussion_id = :discussion_id 
                AND restricted_until > datetime('now')
            """), {"user_id": report.reported_user_id, "discussion_id": discussion_id})
            
            if not restriction_check.fetchone():
                # 24시간 제한 적용
                restriction_end = datetime.now() + timedelta(hours=24)
                conn.execute(text("""
                    INSERT INTO user_chat_restrictions (user_id, discussion_id, restricted_until)
                    VALUES (:user_id, :discussion_id, :restricted_until)
                """), {
                    "user_id": report.reported_user_id,
                    "discussion_id": discussion_id,
                    "restricted_until": restriction_end
                })
                conn.commit()
                print(f"사용자 {report.reported_user_id}가 토론방 {discussion_id}에서 24시간 제한됨")

    return {
        "id": 1,  # 임시 ID
        "reporter_id": current_user.id,
        "reported_user_id": report.reported_user_id,
        "message_id": report.message_id,
        "created_at": datetime.now()
    }

@router.get("/users/{user_id}/report-status/{discussion_id}")
async def get_user_report_status(
    user_id: int,
    discussion_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # 채팅 제한 상태 확인
    with engine.connect() as conn:
        result = conn.execute(text("""
            SELECT restricted_until FROM user_chat_restrictions 
            WHERE user_id = :user_id AND discussion_id = :discussion_id 
            AND restricted_until > datetime('now')
        """), {"user_id": user_id, "discussion_id": discussion_id})
        
        restriction = result.fetchone()
        
        if restriction:
            return {
                "is_restricted": True,
                "restriction_end": restriction[0]
            }
        
        return {
            "is_restricted": False,
            "restriction_end": None
        } 