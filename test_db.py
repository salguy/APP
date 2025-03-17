from sqlalchemy.orm import Session
from database import SessionLocal
from models import User, Medication, MedicationHistory, MedicationSchedule
from datetime import datetime

# 데이터베이스 세션 시작
db: Session = SessionLocal()

# 1️⃣ 사용자 추가
user = User(name="홍길동")
db.add(user)
db.commit()
db.refresh(user)  # id를 가져오기 위해 refresh

# 2️⃣ 약 추가
medication = Medication(name="Tyrenol")
db.add(medication)
db.commit()
db.refresh(medication)

# 3️⃣ 복용 기록 추가
med_history = MedicationHistory(
    user_id=user.id,
    medication_id=medication.id,
    dosage_mg="500",
    taken_at=datetime(2025, 3, 12, 8, 0),  # 2025년 3월 11일 08:00
)
db.add(med_history)
db.commit()

# 4️⃣ 복용 일정 추가
med_schedule = MedicationSchedule(
    user_id=user.id,
    medication_id=medication.id,
    scheduled_time=datetime(2025, 3, 12, 8, 0),  # 2025년 3월 12일 08:00
    dosage_mg="500"
)
db.add(med_schedule)
db.commit()

print("샘플 데이터 추가 완료!")

# 세션 닫기
db.close()
