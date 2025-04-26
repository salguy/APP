from pydantic import BaseModel, Field
from typing import List, Optional, Literal
from models import *

class TestError(Exception):
    """테스트 관련 에러를 처리하기 위한 기본 예외 클래스"""
    pass

class TestInputError(TestError):
    """테스트 입력값 관련 에러"""
    pass

class TestProcessingError(TestError):
    """테스트 처리 과정 중 발생하는 에러"""
    pass

class TestResponseError(TestError):
    """테스트 응답 처리 중 발생하는 에러"""
    pass

class ScheduleID(BaseModel):
    scheduleId: int = Field(..., description="복약 스케줄 ID (-1인 경우 스케줄 검증 생략)")
    
class TestSchema(BaseModel):
    userId: int = Field(..., description="유저 ID")
    scheduleId: int = Field(..., description="복약 스케줄 ID (-1인 경우 스케줄 검증 생략)")
    responsetype: Literal['check_meal', 'induce_medicine', 'taking_medicine_time', 'check_medicine', 'daily_talk'] = Field(
        ..., 
        description="응답 타입: check_meal(복약 전 식사여부 체크), induce_medicine(복약 유도), taking_medicine_time(복약 시점 도달, 아무 음성이나 넣어도 됨), check_medicine(복용 완료 확인), daily_talk(일상 대화)"
    )

class TestResponse(BaseModel):
    message: str = Field(..., description="AI 서버의 응답 메시지")
    file_url: str = Field(..., description="생성된 음성 파일의 URL")
