from sqlalchemy.orm import Session
from models import *

from domain.user.schema import *


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