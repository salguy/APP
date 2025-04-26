from pydantic import BaseModel
from models import *


class MedicationRecordCreate(BaseModel):
    taken_at: str  # 실제 복용 시각
    schedule_id: int

class MedicationRecordGet(BaseModel):
    user_id: int

class MedicationScheduleCreate(BaseModel):
    user_id: int
    medication_id: int
    dosage_mg: int
    scheduled_time: str


class UserDelete(BaseModel):
    user_id: int
    
    
class SignupRequest(BaseModel):
    name: str
    password: str
    
class LoginRequest(BaseModel):
    user_id: str
    password: str