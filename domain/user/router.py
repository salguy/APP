from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from domain.user.crud import *
from domain.user.schema import *

router = APIRouter()

@router.post("/api/user/histories", summary="복약 정보 저장")
async def add_medication_records(record: MedicationRecordCreate, db: Session = Depends(get_db)):
    """
    특정 유저의 복약 정보를 저장하는 엔드포인트입니다.
    - **user_id**:          int, 유저 고유 번호(현재 1만 가능)
    - **medication_id**:    int, 약 고유 번호(현재 1만 가능)
    - **taken_at**:         str, 실제 복용 시각(yy.mm.dd.hh.mm)
    - **schedule_id**:      int, 복용 스케줄 ID 
    - **dosage_mg**:        int, 복용 용량(mg)
    """
    try:
        return create_medication_record(db, record)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    
    
@router.get("/api/user/histories", summary="복약 정보 호출")
async def get_medication_histories(user_id: int, db: Session = Depends(get_db)):
    """
    특정 유저의 복약 정보를 호출하는 엔드포인트입니다.
    - **user_id**:          int, 유저 고유 번호(현재 1만 가능)
    """
    try:
        record = MedicationRecordGet(user_id=user_id)  
        return get_medication_record(db, record)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    
