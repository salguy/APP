from sqlalchemy import Column, DateTime, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, index=True, comment="고유번호")  # 고유번호
    name = Column(String, nullable=False, comment="사용자 이름")  # 이름
    
    medication_schedules = relationship("MedicationSchedule", back_populates="user")

class Medication(Base):
    __tablename__ = "medication"

    id = Column(Integer, primary_key=True, index=True)  # 고유번호
    name = Column(String, nullable=False, comment="약 이름")  # 약 이름

    medication_schedules = relationship("MedicationSchedule", back_populates="medication")

class MedicationSchedule(Base):
    __tablename__ = "medication_schedule"

    id = Column(Integer, primary_key=True, index=True)  # 고유번호
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False, comment="사용자 ID")
    medication_id = Column(Integer, ForeignKey("medication.id"), nullable=False, comment="약 ID")
    dosage_mg = Column(String, nullable=False, comment="복용 용량")
    scheduled_time = Column(DateTime, nullable=False, comment="복용 예정 시간")
    taken_at = Column(DateTime, nullable=True, comment="복용 시각")

    user = relationship("User", back_populates="medication_schedules")
    medication = relationship("Medication", back_populates="medication_schedules")
