from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from domain.medications.crud import *
from domain.medications.schema import *

router = APIRouter()

@router.get("/api/medications", summary="약 정보 호출")
async def get_medication_names(db: Session = Depends(get_db)):
    """
    모든 약의 정보를 호출하는 엔드포인트입니다.
    """
    try:
        return get_medications_all(db)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    
    
@router.post("/api/medications", summary="약 정보 추가")
async def add_medications(record: MedicationAdd, db: Session = Depends(get_db)):
    """
    약의 정보를 추가하는 엔드포인트입니다.
    **pill_name** : str
    """
    try:
        return add_pills(db, record)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))