from pydantic import BaseModel, ConfigDict
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