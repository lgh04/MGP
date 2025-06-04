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

    def check_and_restrict_user(self, user_id):
        """사용자가 3번 신고당했는지 확인하고 제한을 적용합니다."""
        table_name = f"discussion_{self.id}_reports"
        
        with engine.connect() as conn:
            # 해당 사용자가 받은 신고 수 확인
            result = conn.execute(text(f"""
                SELECT COUNT(*) as report_count 
                FROM {table_name} 
                WHERE reported_user_id = :user_id
            """), {"user_id": user_id})
            
            report_count = result.scalar()
            
            if report_count >= 3:
                # 이미 제한이 있는지 확인
                restriction_check = conn.execute(text("""
                    SELECT * FROM user_chat_restrictions 
                    WHERE user_id = :user_id AND discussion_id = :discussion_id 
                    AND restricted_until > datetime('now')
                """), {"user_id": user_id, "discussion_id": self.id})
                
                if not restriction_check.fetchone():
                    # 24시간 제한 적용
                    restriction_end = datetime.now() + timedelta(hours=24)
                    conn.execute(text("""
                        INSERT INTO user_chat_restrictions (user_id, discussion_id, restricted_until)
                        VALUES (:user_id, :discussion_id, :restricted_until)
                    """), {
                        "user_id": user_id,
                        "discussion_id": self.id,
                        "restricted_until": restriction_end
                    })
                    conn.commit()
                    print(f"사용자 {user_id}가 토론방 {self.id}에서 24시간 제한됨")
                    return True
        return False

class UserChatRestriction(Base):
    __tablename__ = "user_chat_restrictions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    discussion_id = Column(Integer, ForeignKey("discussions.id"))
    restricted_until = Column(DateTime)
    created_at = Column(DateTime, default=func.now())

    user = relationship("User")
    discussion = relationship("Discussion")

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