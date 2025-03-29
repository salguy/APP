from pydantic import BaseModel, field_validator
from datetime import datetime
from sqlalchemy.orm import Session
from database import get_db  # 세션 가져오기
from models import *

class MedicationRecordCreate(BaseModel):
    taken_at: str  # 실제 복용 시각
    schedule_id: int
    
    @field_validator("schedule_id")
    def validate_schedule_exists(cls, value):
        db: Session = get_db()  # DB 세션 가져오기
        pill = db.query(MedicationSchedule).filter(MedicationSchedule.id == value).first()
        db.close()  # 세션 닫기

        if not pill:
            raise ValueError(f"존재하지 않는 schedule_id: {value}")
        return value
    
 # 날짜 형식 검증 (YY:MM:DD:HH:MM)
    @field_validator("taken_at")
    def validate_datetime_format(cls, value):
        try:
            return datetime.strptime(value, "%y.%m.%d.%H.%M")  # YY:MM:DD:HH:MM 형식 체크
        except ValueError:
            raise ValueError(f"날짜 형식이 올바르지 않습니다: {value} , (YY.MM.DD.HH.MM 형식이어야 함)")
            
    @field_validator("taken_at")
    def validate_taken_at(cls, value):
        if value > datetime.now():
            raise ValueError(f"taken_at은 현재 시각보다 과거여야 합니다., 현재 시각: {datetime.now()}")
        return value  # 검증 통과 시 그대로 반환
    
    
class MedicationRecordGet(BaseModel):
    user_id: int
    
    # 1️⃣ 유저 존재 여부 검증
    @field_validator("user_id")
    def validate_user_exists(cls, value):
        with get_db() as db:
            user_exists = db.query(User).filter(User.id == value).scalar() is not None

        if not user_exists:
            raise ValueError(f"존재하지 않는 user_id: {value}")  # ✅ ValueError 사용
        return value
    
    
class MedicationScheduleCreate(BaseModel):
    user_id: int
    medication_id: int
    dosage_mg: int
    scheduled_time: str
    
    @field_validator("user_id")
    def validate_user_exists(cls, value):
        with get_db() as db:
            user_exists = db.query(User).filter(User.id == value).scalar() is not None

        if not user_exists:
            raise ValueError(f"존재하지 않는 user_id: {value}")  # ✅ ValueError 사용
        return value
    
    @field_validator("medication_id")
    def validate_medication_exists(cls, value):
        with get_db() as db:
            pills_exists = db.query(Medication).filter(Medication.id == value).scalar() is not None

        if not pills_exists:
            raise ValueError(f"존재하지 않는 medication_id: {value}")  # ✅ ValueError 사용
        return value
    
    @field_validator("scheduled_time")
    def validate_datetime_format(cls, value):
        try:
            return datetime.strptime(value, "%y.%m.%d.%H.%M")  # YY:MM:DD:HH:MM 형식 체크
        except ValueError:
            raise ValueError(f"날짜 형식이 올바르지 않습니다: {value} , (YY.MM.DD.HH.MM 형식이어야 함)")
        

class UserAdd(BaseModel):
    user_name: str