from sqlalchemy.orm import Session
from models import MedicationHistory, MedicationSchedule

def create_medication_record(db: Session, record_data):
    # 1. MedicationHistory 저장
    history = MedicationHistory(
        user_id=record_data.user_id,
        medication_id=record_data.medication_id,
        taken_at=record_data.taken_at,
        dosage_taken=record_data.dosage_taken,
        is_taken=record_data.is_taken
    )
    db.add(history)

    # 2. MedicationSchedule 저장
    schedule = MedicationSchedule(
        user_id=record_data.user_id,
        medication_id=record_data.medication_id,
        scheduled_time=record_data.scheduled_time,
        dosage=record_data.dosage_taken
    )
    db.add(schedule)

    db.commit()
    db.refresh(history)
    db.refresh(schedule)
    return {"history": history.id, "schedule": schedule.id}
