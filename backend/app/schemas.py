from pydantic import BaseModel, ConfigDict , Field
from datetime import datetime

# get responce
class PatientResponse(BaseModel):
    id: int
    name: str
    age: int | None
    gender: str | None
    created_at : datetime

    model_config = ConfigDict(from_attributes=True)  # simply tells Pydantic: "You can get my data from a Python object's attributes."  ||||     allows Pydantic to read values from our SQLAlchemy Patient object.


# post 
class PatientCreate(BaseModel):
    name: str
    age: int | None = None
    gender: str | None = None

class PatientUpdate(BaseModel):
    name: str | None = None
    age: int | None = None
    gender: str | None = None


class CreateGlucoseReading(BaseModel):
    patient_id: int
    glucose_level: float
    timestamp: datetime | None = None
    source: str | None = None


class GlucoseReadingResponse(BaseModel):
    id: int
    patient_id: int
    glucose_level: float
    timestamp: datetime
    source: str | None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

class CreateClinicalRecord(BaseModel):
    patient_id: int
    record_type: str
    description: str
    record_date: datetime


class ClinicalRecordResponse(BaseModel):
    id: int
    patient_id: int
    record_type: str
    description: str
    record_date: datetime
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

class CreateWearableEvent(BaseModel):
    patient_id: int
    event_id: str | None = None
    timestamp: datetime

    heart_rate: float | None = Field(default=None, ge=0)
    hrv: float | None = Field(default=None, ge=0)
    spo2: float | None = Field(default=None, ge=0, le=100)
    steps: int | None = Field(default=None, ge=0)
    glucose_level: float | None = Field(default=None, ge=0)

    sleep_state: str | None = None
    activity_state: str | None = None
    source: str | None = None


class WearableEventResponse(BaseModel):
    id: int
    patient_id: int
    event_id: str | None
    timestamp: datetime

    heart_rate: float | None
    hrv: float | None
    spo2: float | None
    glucose_level: float | None
    steps: int | None

    sleep_state: str | None
    activity_state: str | None
    source: str | None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)