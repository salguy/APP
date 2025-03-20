from sqlalchemy.orm import Session
from models import MedicationHistory, MedicationSchedule

from domain.medicineInfo.schema import *


def create_medication_record(db: Session, record: MedicationRecordCreate):
    # 1. MedicationHistory 저장
    history = MedicationHistory(
        user_id=record.user_id,
        medication_id=record.medication_id,
        taken_at=record.scheduled_time,  # taken_at을 복용 시각으로 설정
        dosage_mg=record.dosage_mg,  # dosage_taken을 복용 용량으로 저장
    )
    db.add(history) 

    # 2. MedicationSchedule 저장
    schedule = MedicationSchedule(
        user_id=record.user_id,
        medication_id=record.medication_id,
        scheduled_time=record.scheduled_time,  # 예정된 복용 시각
        dosage_mg=record.dosage_mg  # 복용 용량
    )
    db.add(schedule)

    db.commit()  # 트랜잭션 커밋
    db.refresh(history)  # 기록을 새로 고침
    db.refresh(schedule)  # 일정도 새로 고침

    return {"user_id": record.user_id, "history_id": history.id, "schedule_id": schedule.id}  # 기록과 일정 ID 반환


def get_medication_record(db: Session, record: MedicationRecordGet):
    """
    특정 유저의 복약 정보를 데이터베이스에서 조회하는 함수입니다.

    Parameters:
        - db: 데이터베이스 세션
        - record: MedicationRecordGet (user_id와 schedule_id를 포함하는 pydantic 모델)

    Returns:
        조회된 복약 정보 리스트 또는 예외 발생
    """
    
    # 특정 유저(user_id)와 스케줄(schedule_id)에 맞는 복약 이력을 조회
    medication_records = db.query(MedicationSchedule).filter(
        MedicationSchedule.user_id == record.user_id,
        MedicationSchedule.scheduled_time == record.schedule_id
    ).all()

    if not medication_records:
        raise ValueError(f"해당 조건(user_id={record.user_id}, schedule_id={record.schedule_id})에 맞는 복약 정보를 찾을 수 없습니다.")

    return medication_records