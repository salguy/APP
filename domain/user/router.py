from fastapi import APIRouter, Depends, HTTPException, Response, Request
from sqlalchemy.orm import Session
from database import get_db
from domain.user.crud import *
from domain.user.schema import *
from datetime import datetime
from fastapi.security import OAuth2PasswordRequestForm
from domain.state import queues
import asyncio
from jose import JWTError, jwt
from fastapi.responses import JSONResponse

router = APIRouter()


@router.post("/api/user/signup")
def signup(data: SignupRequest, db: Session = Depends(get_db)):

    return signup_user(db, data)


@router.post("/api/user/login")
def login(data: LoginRequest, response: Response, db: Session = Depends(get_db)):
    try:
        user_id = data.user_id
        login_result = login_user(db, data)  # 여기서 토큰 발급
        response.set_cookie(
            key="access_token",
            value=login_result["access_token"],
            httponly=True,
            secure=True,
            samesite="Lax"
        )
        if not login_result["access_token"]:
            # ✅ 여기서 queues에 등록
            if user_id not in queues:
                queues[user_id] = asyncio.Queue()
                print(f"Login | user_id : {user_id} connected")
        return login_result
    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e))


@router.get("/api/user/verify")
async def verify(request: Request, db: Session = Depends(get_db)):
    try:
        return verify_user(request, db)
    except ValueError as e:
        if str(e) == "No token found":
            raise HTTPException(status_code=401, detail=str(e))
        elif str(e) == "Invalid token":
            raise HTTPException(status_code=404, detail=str(e))
        elif str(e) == "Token decode error":
            raise HTTPException(status_code=401, detail=str(e))
        elif "User(id" in str(e):
            raise HTTPException(status_code=404, detail=str(e))
        else:
            raise HTTPException(status_code=500, detail=str(e))
        


@router.put("/api/user/histories", summary="복약 시각 저장")
async def add_medication_history(record: MedicationRecordCreate, db: Session = Depends(get_db)):
    try:
        # schedule_id 존재 확인
        schedule = db.query(MedicationSchedule).filter(MedicationSchedule.id == record.schedule_id).first()
        if not schedule:
            raise ValueError(f"존재하지 않는 schedule_id: {record.schedule_id}")

        # 날짜 포맷 검증
        try:
            record.taken_at = datetime.strptime(record.taken_at, "%y.%m.%d.%H.%M")
        except ValueError:
            raise ValueError(f"날짜 형식이 올바르지 않습니다: {record.taken_at} , (YY.MM.DD.HH.MM 형식이어야 함)")

        if record.taken_at > datetime.now():
            raise ValueError("taken_at은 현재 시각보다 과거여야 합니다.")

        return fill_taken_at(db, record)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/api/user/histories", summary="복약 정보 호출")
async def get_medication_histories(user_id: int, db: Session = Depends(get_db)):
    try:
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise ValueError(f"존재하지 않는 user_id: {user_id}")

        record = MedicationRecordGet(user_id=user_id)
        return get_medication_history(db, record)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/api/users/schedules", summary="복약 일정 저장")
async def add_medication_records(record: MedicationScheduleCreate, db: Session = Depends(get_db)):
    try:
        user = db.query(User).filter(User.id == record.user_id).first()
        if not user:
            raise ValueError(f"존재하지 않는 user_id: {record.user_id}")

        med = db.query(Medication).filter(Medication.id == record.medication_id).first()
        if not med:
            raise ValueError(f"존재하지 않는 medication_id: {record.medication_id}")

        try:
            record.scheduled_time = datetime.strptime(record.scheduled_time, "%y.%m.%d.%H.%M")
        except ValueError:
            raise ValueError(f"날짜 형식이 올바르지 않습니다: {record.scheduled_time} , (YY.MM.DD.HH.MM 형식이어야 함)")

        return submit_medication_schedule(db, record)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/api/users", summary="전체 유저 목록")
async def search_users(db: Session = Depends(get_db)):
    try:
        return search_all_users(db)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/api/users", summary="유저 삭제")
async def delete_users(record: UserDelete, db: Session = Depends(get_db)):
    try:
        return delete_user(db, record)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
