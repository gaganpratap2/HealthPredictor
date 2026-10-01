from fastapi import Depends, FastAPI , HTTPException
from sqlalchemy.orm import Session
from .schemas import GlucoseReadingResponse, PatientResponse , PatientCreate , PatientUpdate , CreateGlucoseReading

from .database import get_db
from .models import GlucoseReading, Patient


app = FastAPI()


@app.get("/")
def root():
    return {"message": "HealthPredictor API is running"}


@app.get("/health")
def health():
    return {"status": "healthy"}


@app.get("/patients" , response_model=list[PatientResponse])
def get_patients(db: Session = Depends(get_db)):
    patients = db.query(Patient).all()

    return patients


@app.post("/patients", response_model=PatientResponse)
def create_patient(
    patient: PatientCreate,
    db: Session = Depends(get_db)
):
    new_patient = Patient(
        name=patient.name,
        age=patient.age,
        gender=patient.gender
    )

    db.add(new_patient)
    db.commit()
    db.refresh(new_patient)

    return new_patient


@app.get("/patients/{patient_id}", response_model=PatientResponse)
def get_patientById(patient_id: int, db: Session = Depends(get_db)):
    patient = db.query(Patient).filter(Patient.id == patient_id).first()

    if patient is None:
      raise HTTPException(
        status_code=404,
        detail="Patient not found"
    )

    return patient

@app.delete("/patients/{patient_id}")
def delete_patient(
    patient_id: int,
    db: Session = Depends(get_db)
):
    patient = db.query(Patient).filter(Patient.id == patient_id).first()

    if patient is None:
        raise HTTPException(
            status_code=404,
            detail="Patient not found"
        )

    db.delete(patient)
    db.commit()

    return {"message": "Patient deleted successfully"}


@app.patch("/patients/{patient_id}", response_model=PatientResponse)
def update_patient(
    patient_id: int,
    patient_data: PatientUpdate,
    db: Session = Depends(get_db)
):
    patient = (
        db.query(Patient)
        .filter(Patient.id == patient_id)
        .first()
    )

    if patient is None:
        raise HTTPException(
            status_code=404,
            detail="Patient not found"
        )

    update_data = patient_data.model_dump(exclude_unset=True) # Give me only the fields the client actually sent.

    for field, value in update_data.items():
        setattr(patient, field, value)

    db.commit()
    db.refresh(patient)

    return patient





@app.post("/glucose-readings",response_model=GlucoseReadingResponse
)
def create_glucose_reading(
    reading: CreateGlucoseReading,
    db: Session = Depends(get_db)
):
    patient = db.query(Patient).filter(
        Patient.id == reading.patient_id
    ).first()

    if patient is None:
        raise HTTPException(
            status_code=404,
            detail="Patient not found"
        )

    new_reading = GlucoseReading(
        patient_id=reading.patient_id,
        glucose_level=reading.glucose_level,
        timestamp=reading.timestamp,
        source=reading.source
    )

    db.add(new_reading)
    db.commit()
    db.refresh(new_reading)

    return new_reading



@app.get("/patients/{patient_id}/glucose-readings", response_model=list[GlucoseReadingResponse]
)
def get_patient_glucose_readings(
    patient_id: int,
    db: Session = Depends(get_db)):
    patient = db.query(Patient).filter(
        Patient.id == patient_id
    ).first()

    if patient is None:
        raise HTTPException(
            status_code=404,
            detail="Patient not found"
        )

    readings = db.query(GlucoseReading).filter(
        GlucoseReading.patient_id == patient_id
    ).order_by(GlucoseReading.timestamp.desc()).all()

    return readings