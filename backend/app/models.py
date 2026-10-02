from datetime import datetime
from sqlalchemy import DateTime, Integer, String , Float, ForeignKey, Text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

class Base(DeclarativeBase):
    pass # lets us get relatively close to what the computer is actually doing while still providing high-level abstractions.
# pass do nothing here, just a placeholder for the base class.

class Patient(Base):
    __tablename__ = "patients"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    age: Mapped[int | None] = mapped_column(Integer)
    gender: Mapped[str | None] = mapped_column(String(20))

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow
    )

    glucose_readings: Mapped[list["GlucoseReading"]] = relationship(
        back_populates="patient"
    )

    clinical_records: Mapped[list["ClinicalRecord"]] = relationship(
        back_populates="patient"
    )

    wearable_events: Mapped[list["WearableEvent"]] = relationship(
    back_populates="patient"
    )

class GlucoseReading(Base):

    __tablename__ = "glucose_readings"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    patient_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("patients.id"),
        nullable=False
    )
    glucose_level: Mapped[float] = mapped_column(
        Float,
        nullable=False
    )
    timestamp: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow
    )

    source: Mapped[str | None] = mapped_column(String(100))

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow
    )
    patient: Mapped["Patient"] = relationship(
    back_populates="glucose_readings"
    )


class ClinicalRecord(Base):
    __tablename__ = "clinical_records"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True
    )

    patient_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("patients.id"),
        nullable=False
    )

    record_type: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    description: Mapped[str] = mapped_column(
        Text,
        nullable=False
    )

    record_date: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow
    )
    patient: Mapped["Patient"] = relationship(
    back_populates="clinical_records"
    )



class WearableEvent(Base):
    __tablename__ = "wearable_events"

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True
    )

    patient_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("patients.id"),
        nullable=False
    )

    event_id: Mapped[str | None] = mapped_column(
        Text, unique=True, nullable=True
    )

    timestamp: Mapped[datetime] = mapped_column(
        DateTime, nullable=False
    )

    heart_rate: Mapped[float | None] = mapped_column(Float)
    hrv: Mapped[float | None] = mapped_column(Float)
    spo2: Mapped[float | None] = mapped_column(Float)
    glucose_level: Mapped[float | None] = mapped_column(Float)
    steps: Mapped[int | None] = mapped_column(Integer)

    sleep_state: Mapped[str | None] = mapped_column(
        String(30)
    )
    activity_state: Mapped[str | None] = mapped_column(
        String(30)
    )
    source: Mapped[str | None] = mapped_column(
        String(200)
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow
    )

    patient: Mapped["Patient"] = relationship(
        back_populates="wearable_events"
    )