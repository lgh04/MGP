from pydantic import BaseModel

class UserCreate(BaseModel):
    name: str
    phone: str
    email: str
    password: str
    confirm_password: str
    nickname: str
    phone_auth_code: str


class UserLogin(BaseModel):
    email: str
    password: str

class PhoneAuthRequest(BaseModel):
    phone_number: str

class PhoneAuthVerify(BaseModel):
    phone_number: str
    code: str
