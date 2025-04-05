from pydantic import BaseModel
from models import *


class ScheduleID(BaseModel):
    scheduleId: int