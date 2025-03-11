from sqlalchemy import Boolean, Column, Date, DateTime, Integer, String, ForeignKey, Table, func, Text
from sqlalchemy.orm import relationship
from database import Base


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, index=True, nullable=False, comment="사용자 닉네임")
    password = Column(String, nullable=False, comment="비밀번호")
    email = Column(String, unique=True, nullable=False, comment="이메일")

    medications = relationship("Medication", back_populates="user")
    medication_histories = relationship("MedicationHistory", back_populates="user")



class Medication(Base):
    __tablename__ = "medication"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, comment="약 이름")
    dosage = Column(String, nullable=False, comment="약 용량")
    type = Column(String, nullable=False, comment="약 종류")  # 예: 알약, 액체 등

    user_id = Column(Integer, ForeignKey("user.id"), nullable=False, comment="사용자 ID")
    user = relationship("User", back_populates="medications")
    medication_histories = relationship("MedicationHistory", back_populates="medication")

class MedicationHistory(Base):
    __tablename__ = "medication_history"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False, comment="사용자 ID")
    medication_id = Column(Integer, ForeignKey("medication.id"), nullable=False, comment="복용한 약 ID")
    taken_at = Column(DateTime, default=func.now(), comment="복용 시각")
    dosage_taken = Column(String, nullable=False, comment="복용한 용량")
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

