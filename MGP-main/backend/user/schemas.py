from pydantic import BaseModel, EmailStr

class UserBase(BaseModel):
    email: str
    name: str
    phone: str
    nickname: str

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int

    class Config:
        from_attributes = True
