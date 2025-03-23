from sqlalchemy.orm import Session
from models import *

from domain.medications.schema import *

def get_medications_all(db: Session):
    medication_list = db.query(Medication).all()

    if not medication_list:
        raise ValueError(f"등록된 약을 찾을 수 없습니다.")

    return {"medication_list": medication_list}