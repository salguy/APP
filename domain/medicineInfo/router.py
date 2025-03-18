from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from domain.medicineInfo.crud import create_medication_record
from domain.medicineInfo.schema import MedicationRecordCreate

router = APIRouter()

@router.post("/api/medication_record")
def add_medication_record(record: MedicationRecordCreate, db: Session = Depends(get_db)):
    try:
        return create_medication_record(db, record)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))