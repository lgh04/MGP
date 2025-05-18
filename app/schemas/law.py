from pydantic import BaseModel

class LawResponse(BaseModel):
    title: str
    description: str



"""
/schemas/law.py
역할:
법안 정보를 표현하는 데이터 모델 스키마 정의.

구성:
LawResponse: 법안 응답 시 사용되는 Pydantic 모델
title (str): 법안 제목
description (str): 법안 설명

용도:
API 응답에서 법안 관련 정보를 직렬화하고 검증하는 데 사용된다.
"""
