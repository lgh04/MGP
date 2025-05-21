# 법안의 제목과 설명을 담는 응답용 데이터 모델

from pydantic import BaseModel # Pydantic의 BaseModel을 상속받아 데이터 모델 정의

# 법안 응답 데이터 모델
class LawResponse(BaseModel):
    title: str # 법안 제목
    description: str # 법안 설명



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
