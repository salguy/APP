from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from crud import create_medication_record
from schema import MedicationRecordCreate

router = APIRouter()

@router.post("/medication_record/")
def add_medication_record(record: MedicationRecordCreate, db: Session = Depends(get_db)):
    return create_medication_record(db, record)
