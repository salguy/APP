from sqlalchemy.orm import Session
from database import SessionLocal
from models import User, Medication, MedicationSchedule
from datetime import datetime

# 데이터베이스 세션 시작
db: Session = SessionLocal()

# 1️⃣ 사용자 추가
user = User(name="홍길동", password="1234")
db.add(user)
db.commit()
db.refresh(user)  # id를 가져오기 위해 refresh

# 2️⃣ 약 추가
medication = Medication(name="Tyrenol")
db.add(medication)
db.commit()
db.refresh(medication)


# 4️⃣ 복용 일정 추가
med_schedule = MedicationSchedule(
    user_id=user.id,
    medication_id=medication.id,
    scheduled_time=datetime(2025, 3, 12, 8, 0),  # 2025년 3월 12일 08:00
    dosage_mg="500",
    taken_at=datetime(2025,3,12,8,0)
)
db.add(med_schedule)
db.commit()



print("샘플 데이터 추가 완료!")

# 세션 닫기
db.close()
