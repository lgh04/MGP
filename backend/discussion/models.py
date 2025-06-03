from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, func, Table, MetaData, Boolean
from sqlalchemy.orm import relationship
from backend.db.database import Base, engine
from datetime import datetime, timedelta
from sqlalchemy.sql import text

class Discussion(Base):
    __tablename__ = "discussions"

    id = Column(Integer, primary_key=True, index=True)
    bill_id = Column(String, index=True)
    created_at = Column(DateTime, default=func.now())

    participants = relationship("DiscussionParticipant", back_populates="discussion")
    messages = relationship("DiscussionMessage", back_populates="discussion")

    def create_report_table(self):
        """토론방별 신고 테이블을 생성합니다."""
        table_name = f"discussion_{self.id}_reports"
        
        # 테이블이 이미 존재하는지 확인
        with engine.connect() as conn:
            result = conn.execute(text(f"""
                SELECT name FROM sqlite_master 
                WHERE type='table' AND name='{table_name}'
            """))
            exists = result.scalar() is not None

            if not exists:
                conn.execute(text(f"""
                    CREATE TABLE {table_name} (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        reporter_id INTEGER REFERENCES users(id),
                        reported_user_id INTEGER REFERENCES users(id),
                        message_id INTEGER REFERENCES discussion_messages(id),
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                """))
                conn.commit()
                print(f"신고 테이블 생성됨: {table_name}")
            else:
                print(f"테이블이 이미 존재함: {table_name}")

    def check_and_restrict_user(self, db, user_id: int) -> bool:
        """사용자의 신고 횟수를 확인하고 필요시 채팅을 제한합니다."""
        table_name = f"discussion_{self.id}_reports"
        
        # 해당 사용자에 대한 신고 횟수 조회
        count_query = text(f"""
            SELECT COUNT(DISTINCT reporter_id) 
            FROM {table_name} 
            WHERE reported_user_id = :user_id
        """)
        
        result = db.execute(count_query, {"user_id": user_id}).scalar()
        
        # 3회 이상 신고 받았다면 채팅 제한
        if result >= 3:
            # 기존 제한이 있는지 확인
            existing_restriction = db.query(UserChatRestriction).filter(
                UserChatRestriction.user_id == user_id,
                UserChatRestriction.discussion_id == self.id,
                UserChatRestriction.restricted_until > datetime.now()
            ).first()

            if not existing_restriction:
                restriction = UserChatRestriction(
                    user_id=user_id,
                    discussion_id=self.id,
                    restricted_until=datetime.now() + timedelta(hours=24)
                )
                db.add(restriction)
                db.commit()
            return True
            
        return False

class DiscussionParticipant(Base):
    __tablename__ = "discussion_participants"

    id = Column(Integer, primary_key=True, index=True)
    discussion_id = Column(Integer, ForeignKey("discussions.id"))
    user_id = Column(Integer, ForeignKey("users.id"))
    joined_at = Column(DateTime, default=func.now())

    discussion = relationship("Discussion", back_populates="participants")
    user = relationship("User")

class DiscussionMessage(Base):
    __tablename__ = "discussion_messages"

    id = Column(Integer, primary_key=True, index=True)
    discussion_id = Column(Integer, ForeignKey("discussions.id"))
    user_id = Column(Integer, ForeignKey("users.id"))
    content = Column(String)
    created_at = Column(DateTime, default=func.now())

    discussion = relationship("Discussion", back_populates="messages")
    user = relationship("User")

class UserChatRestriction(Base):
    __tablename__ = "user_chat_restrictions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    discussion_id = Column(Integer, ForeignKey("discussions.id"))
    restricted_until = Column(DateTime)
    created_at = Column(DateTime, default=func.now())

    @classmethod
    def is_restricted(cls, db, user_id: int, discussion_id: int) -> bool:
        """사용자가 현재 채팅 제한 상태인지 확인합니다."""
        restriction = db.query(cls).filter(
            cls.user_id == user_id,
            cls.discussion_id == discussion_id,
            cls.restricted_until > datetime.now()
        ).first()
        return bool(restriction) 