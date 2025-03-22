from sqlalchemy.orm import Session
from models import MedicationHistory, MedicationSchedule

from domain.user.schema import *


def create_medication_record(db: Session, record: MedicationRecordCreate):
    
    # 2. MedicationSchedule 저장
    schedule = MedicationSchedule(
        user_id=record.user_id,
        medication_id=record.medication_id,
        taken_at = record.taken_at, # 예정된 복용 시각
        schedule_id=record.schedule_id,  
        dosage_mg=record.dosage_mg  # 복용 용량
    )
    db.add(schedule)

    db.commit()  # 트랜잭션 커밋
    db.refresh(schedule)  # 일정도 새로 고침

    return {"user_id": record.user_id, "schedule_id": schedule.id}  # 기록과 일정 ID 반환


def get_medication_record(db: Session, record: MedicationRecordGet):
    
    # 특정 유저(user_id)와 스케줄(schedule_id)에 맞는 복약 이력을 조회
    medication_records = db.query(MedicationSchedule).all()

    if not medication_records:
        raise ValueError(f"해당 조건(user_id={record.user_id}) 에 맞는 복약 정보를 찾을 수 없습니다.")

    return {"medication record": medication_records}
