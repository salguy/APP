from pydantic import BaseModel, field_validator
from datetime import datetime
from fastapi import HTTPException
from sqlalchemy.orm import Session
from database import get_db  # 세션 가져오기
from models import User, Medication  # User 모델 가져오기

class MedicationRecordCreate(BaseModel):
    user_id: int
    medication_id: int
    taken_at: str  # 실제 복용 시각
    scheduled_time: str  # 원래 복용해야 할 시각
    dosage_mg: int
    
    
    # 1️⃣ 유저 존재 여부 검증
    @field_validator("user_id")
    @classmethod
    def validate_user_exists(cls, value):
        db: Session = get_db()  # DB 세션 가져오기
        user = db.query(User).filter(User.id == value).first()
        db.close()  # 세션 닫기

        if not user:
            raise HTTPException(
                status_code=400,
                detail=f"존재하지 않는 user_id: {value}"
            )
        return value
# 약 존재 여부 검증
    @field_validator("medication_id")
    @classmethod
    def validate_user_exists(cls, value):
        db: Session = get_db()  # DB 세션 가져오기
        user = db.query(Medication).filter(Medication.id == value).first()
        db.close()  # 세션 닫기

        if not user:
            raise HTTPException(
                status_code=400,
                detail=f"존재하지 않는 medication_id: {value}"
            )
        return value
    
 # 날짜 형식 검증 (YY:MM:DD:HH:MM)
    @field_validator("taken_at", "scheduled_time")
    @classmethod    
    def validate_datetime_format(cls, value):
        try:
            return datetime.strptime(value, "%y.%m.%d.%H.%M")  # YY:MM:DD:HH:MM 형식 체크
        except ValueError:
            raise HTTPException(
                status_code=400,
                detail=f"날짜 형식이 올바르지 않습니다: {value} , (YY.MM.DD.HH.MM 형식이어야 함)"
            )