from sqlalchemy.orm import Session
from models import *
from jose import jwt, JWTError
from fastapi.responses import JSONResponse
from fastapi import Request

from domain.user.schema import *
from passlib.context import CryptContext
from jose import jwt
from dotenv import load_dotenv
import os

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def signup_user(db: Session, record: SignupRequest):
    hashed = pwd_context.hash(record.password)
    user = User(
        name=record.name,
        password=hashed
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return {"user_id": user.id, "message": "회원가입 완료"}

def login_user(db: Session, record: LoginRequest):
    user = db.query(User).filter(User.id == record.user_id).first()
    if not user or not pwd_context.verify(record.password, user.password):
        raise ValueError(f"존재하지 않는 ID 혹은 비밀번호가 일치하지 않습니다.")
    
    token = jwt.encode({"user_id": user.id}, SECRET_KEY, algorithm=ALGORITHM)
    response = JSONResponse(content={"access_token": token, "token_type": "bearer"})
    response.set_cookie(
            key="access_token",
            value=token,
            httponly=True,
            secure=False,
            samesite="Lax"
        )
    return response


def verify_user(request: Request, db: Session):
    token = request.cookies.get("access_token")
    if not token:
        raise ValueError("No token found")
    
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("user_id")
        if user_id is None:
            raise ValueError("Invalid token")
    except JWTError:
        raise ValueError("Token decode error")

    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise ValueError(f"User(id:{user.id}) not found")

    return JSONResponse(content={"message": "Authenticated"}, status_code=200)

def get_my_info(request: Request, db: Session):
    try:
        token = request.cookies.get("access_token")
        if not token:
            raise ValueError("No token found")
        
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("user_id")
        if user_id is None:
            raise ValueError("Invalid token")
        
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise ValueError(f"존재하지 않는 user_id: {user_id}")
        profile_img = '/static/profile_img/' + str(user.id) + '.jpg'
        return {"user_id": user.id, "name": user.name, "profile_img": profile_img}
    except JWTError:
        raise ValueError("Token decode error")
    
def fill_taken_at(db: Session, record: MedicationRecordCreate):
    
    # 해당 스케줄을 조회
    schedule = db.query(MedicationSchedule).filter(MedicationSchedule.id == record.schedule_id).first()
    if schedule is None:
        raise ValueError(f"조건 (schedule_id: {record.schedule_id})에 맞는 스케줄을 찾을 수 없습니다.")

    # 이미 값이 채워져 있다면 업데이트하지 않거나, 경고를 줄 수 있음
    if schedule.taken_at is not None:
        raise ValueError(f"taken_at이 이미 채워져 있습니다.")

    # taken_at 값 업데이트
    schedule.taken_at = record.taken_at
    db.commit()
    db.refresh(schedule)
    return {"schedule_id": schedule.id, "taken_at": schedule.taken_at}


def get_medication_history(db: Session, record: MedicationRecordGet):
    
    # 특정 유저(user_id)와 스케줄(schedule_id)에 맞는 복약 이력을 조회
    medication_records = db.query(MedicationSchedule).all()

    if not medication_records:
        raise ValueError(f"해당 조건(user_id={record.user_id}) 에 맞는 복약 정보를 찾을 수 없습니다.")

    return {"medication record": medication_records}


def submit_medication_schedule(db: Session, record: MedicationScheduleCreate):
    
    schedule = MedicationSchedule(
        user_id = record.user_id,
        medication_id = record.medication_id,
        dosage_mg = record.dosage_mg,
        scheduled_time = record.scheduled_time        
    )
    db.add(schedule)
    db.commit()
    db.refresh(schedule)
    return f"schedule 추가 완료! id: {schedule.id}"

def search_all_users(db: Session):
    users_list = db.query(User).all()

    if not users_list:
        raise ValueError(f"등록된 유저가 없습니다.")

    return {"users_list": users_list}



def delete_user(db: Session, record: UserDelete):
    user=db.query(User).filter(User.id == record.user_id).first()
    if not user:
        raise ValueError(f"User (id: {record.user_id}) not found")
    
    # 사용자 삭제
    db.delete(user)
    db.commit()
    
    return {"message": f"User deleted successfully, id: {record.user_id}"}