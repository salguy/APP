from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from domain.medicineInfo.crud import *
from domain.medicineInfo.schema import *

router = APIRouter()

@router.post("/api/medication_record", summary="복약 정보 저장")
async def add_medication_record(record: MedicationRecordCreate, db: Session = Depends(get_db)):
    """
    특정 유저의 복약 정보를 저장하는 엔드포인트입니다.
    - **user_id**:          int, 유저 고유 번호(현재 1만 가능)
    - **medication_id**:    int, 약 고유 번호(현재 1만 가능)
    - **taken_at**:         str, 실제 복용 시각(yy.mm.dd.hh.mm)
    - **scheduled_time**:   str, 복용 예정 시각(yy.mm.dd.hh.mm)
    - **dosage_mg**:        int, 복용 용량(mg)
    """
    try:
        return create_medication_record(db, record)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    
    
@router.get("/api/get_medication_history", summary="복약 정보 호출")
async def get_medication_history(user_id: int, schedule_id: int, db: Session = Depends(get_db)):
    """
    특정 유저의 복약 정보를 호출하는 엔드포인트입니다.
    - **user_id**:          int, 유저 고유 번호(현재 1만 가능)
    - **schedule_id**:      int, 스케줄 번호   
    """
    try:
        record = MedicationRecordGet(user_id=user_id, schedule_id=schedule_id)  
        return get_medication_record(db, record)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))