from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from domain.user.crud import *
from domain.user.schema import *

router = APIRouter()

@router.put("/api/user/histories", summary="복약 시각 저장")
async def add_medication_history(record: MedicationRecordCreate, db: Session = Depends(get_db)):
    """
    특정 유저의 복약 기록을 저장하는 엔드포인트입니다.
    - **taken_at**:         str, 실제 복용 시각(yy.mm.dd.hh.mm)
    - **schedule_id**:      int, 복용 스케줄 ID 
    """
    try:
        return fill_taken_at(db, record)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    
    
@router.get("/api/user/histories", summary="복약 정보 호출")
async def get_medication_histories(user_id: int, db: Session = Depends(get_db)):
    """
    특정 유저의 모든 복약 정보를 호출하는 엔드포인트입니다.
    - **user_id**:          int, 유저 고유 번호(현재 1만 가능)
    """
    try:
        record = MedicationRecordGet(user_id=user_id)  
        return get_medication_history(db, record)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    


#POST /api/users/schedules : 새로운 복약 스케줄 생성

@router.post("/api/users/schedules", summary="복약 일정 저장")
async def add_medication_records(record: MedicationScheduleCreate, db: Session = Depends(get_db)):
    """
    특정 유저의 복약 기록을 저장하는 엔드포인트입니다.
    - **user_id**:          int, 유저 고유 번호(현재 1만 가능)
    - **medication_id**:    int, 약 고유 번호(현재 1만 가능)
    - **taken_at**:         str, 실제 복용 시각(yy.mm.dd.hh.mm)
    - **schedule_id**:      int, 복용 스케줄 ID 
    - **dosage_mg**:        int, 복용 용량(mg)
    """
    try:
        return submit_medication_schedule(db, record)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    
    
@router.get("/api/users", summary="전체 유저 목록")
async def search_users(db: Session = Depends(get_db)):
    try:
        return search_all_users(db)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@router.post("/api/users", summary="유저 추가")
async def add_users(record: UserAdd, db: Session = Depends(get_db)):
    try:
        return add_user(db, record)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))