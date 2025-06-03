from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional

class MessageBase(BaseModel):
    content: str

class MessageCreate(MessageBase):
    pass

class Message(MessageBase):
    id: int
    discussion_id: int
    user_id: int
    user_nickname: str
    created_at: datetime

    class Config:
        from_attributes = True

class DiscussionBase(BaseModel):
    bill_id: str

class DiscussionCreate(DiscussionBase):
    pass

class Discussion(DiscussionBase):
    id: int
    created_at: datetime
    participant_count: int
    is_participating: bool

    class Config:
        from_attributes = True

class DiscussionDetail(Discussion):
    messages: List[Message]

class DiscussionParticipant(BaseModel):
    user_id: int
    user_nickname: str
    joined_at: datetime

    class Config:
        from_attributes = True

class MyDiscussion(BaseModel):
    id: int
    bill_id: str
    bill_name: str
    participant_count: int
    last_message: Optional[str]
    last_message_time: Optional[datetime]

    class Config:
        from_attributes = True

class ReportCreate(BaseModel):
    reported_user_id: int
    message_id: int

class Report(BaseModel):
    id: int
    reporter_id: int
    reported_user_id: int
    message_id: int
    created_at: datetime

    class Config:
        from_attributes = True 