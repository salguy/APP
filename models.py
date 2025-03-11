from sqlalchemy import Boolean, Column, Date, DateTime, Integer, String, ForeignKey, Table, func, Text
from sqlalchemy.orm import relationship
from database import Base


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=False, index=True, nullable=False, comment="사용자 이름")
    password = Column(String, nullable=False, comment="비밀번호")
    medications = relationship("Medication", back_populates="user")
    medication_histories = relationship("MedicationHistory", back_populates="user")



class Medication(Base):
    __tablename__ = "medication"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, comment="약 이름")

    user_id = Column(Integer, ForeignKey("user.id"), nullable=False, comment="사용자 ID")
    user = relationship("User", back_populates="medications")
    medication_histories = relationship("MedicationHistory", back_populates="medication")

class MedicationHistory(Base):
    __tablename__ = "medication_history"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False, comment="사용자 ID")
    medication_id = Column(Integer, ForeignKey("medication.id"), nullable=False, comment="복용한 약 ID")
    dosage = Column(String, nullable=False, comment="약 용량(mg)")
    taken_at = Column(DateTime, default=func.now(), comment="복용 시각")
    is_taken = Column(Boolean, default=False, comment="복용 여부")
    user = relationship("User", back_populates="medication_histories")
    medication = relationship("Medication", back_populates="medication_histories")

class MedicationSchedule(Base):
    __tablename__ = "medication_schedule"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False, comment="사용자 ID")
    medication_id = Column(Integer, ForeignKey("medication.id"), nullable=False, comment="복용할 약 ID")
    scheduled_time = Column(DateTime, nullable=False, comment="복용 시각")
    dosage = Column(String, nullable=False, comment="예정된 복용 용량")

    user = relationship("User", back_populates="medication_schedules")
    medication = relationship("Medication", back_populates="medication_schedules")

