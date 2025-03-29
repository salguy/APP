from pydantic import BaseModel
from database import get_db  # 세션 가져오기
from models import *

class MedicationAdd(BaseModel):
    medication_name: str
    
    
class MedicationDelete(BaseModel):
    medication_id: int
    