from pydantic import BaseModel
from models import *


class ScheduleID(BaseModel):
    scheduleId: int
    
    
class TestSchema(BaseModel):
    scheduleId: int
    responsetype: str
