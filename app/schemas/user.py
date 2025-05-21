# 회원가입, 로그인, 휴대폰 인증 요청/확인에 사용되는 사용자 관련 Pydantic 요청 모델들 정의

from pydantic import BaseModel # Pydantic 기반의 데이터 모델 생성용 클래스

# 회원가입 요청 모델
class UserCreate(BaseModel):
    name: str # 사용자 이름
    phone: str  # 휴대폰 번호
    email: str # 이메일
    password: str # 비밀번호
    confirm_password: str # 비밀번호 확인
    nickname: str # 닉네임
    phone_auth_code: str # 인증번호 (휴대폰 인증 시 입력값)

# 로그인 요청 모델
class UserLogin(BaseModel): 
    email: str # 이메일
    password: str  # 비밀번호

# 휴대폰 인증번호 전송 요청 모델
class PhoneAuthRequest(BaseModel):
    phone_number: str # 인증번호를 보낼 대상 전화번호

# 휴대폰 인증번호 확인 요청 모델
class PhoneAuthVerify(BaseModel):
    phone_number: str # 전화번호
    code: str # 입력된 인증번호


"""
/schemas/user.py
역할:
사용자 관련 요청과 응답에 쓰이는 데이터 모델 스키마 정의.

구성:
=====UserCreate: 회원가입 요청 데이터 모델
name (str): 이름
phone (str): 휴대폰 번호
email (str): 이메일
password (str): 비밀번호
confirm_password (str): 비밀번호 확인
nickname (str): 닉네임
phone_auth_code (str): 휴대폰 인증 코드

=====UserLogin: 로그인 요청 데이터 모델
email (str): 이메일
password (str): 비밀번호

=====PhoneAuthRequest: 인증번호 전송 요청 데이터 모델
phone_number (str): 휴대폰 번호

=====PhoneAuthVerify: 인증번호 확인 요청 데이터 모델
phone_number (str): 휴대폰 번호
code (str): 인증번호 코드

용도:
사용자 인증 및 회원가입, 로그인, 휴대폰 인증 관련 API 요청 데이터의 검증과 직렬화에 사용된다.
"""
