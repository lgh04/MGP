from pydantic import BaseModel

class UserCreate(BaseModel):
    username: str
    password: str

class UserLogin(BaseModel):
    username: str
    password: str

class PhoneAuthRequest(BaseModel):
    phone_number: str

class PhoneAuthVerify(BaseModel):
    phone_number: str
    code: str
