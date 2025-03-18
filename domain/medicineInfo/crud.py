from sqlalchemy.orm import Session
from models import MedicationHistory, MedicationSchedule

from domain.medicineInfo.schema import MedicationRecordCreate


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
