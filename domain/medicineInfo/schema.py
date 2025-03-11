from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional


class MedicationRecordCreate(BaseModel):
    user_id: int
    medication_id: int
    taken_at: datetime  # 실제 복용 시각
    scheduled_time: datetime  # 원래 복용해야 할 시각
    dosage_taken: str
    is_taken: bool  # 복용 여부
