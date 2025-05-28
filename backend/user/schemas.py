from pydantic import BaseModel, EmailStr

class UserCreate(BaseModel):
    name: str
    phone: str
    email: EmailStr
    password: str
    nickname: str
