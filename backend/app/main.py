from fastapi import Depends, FastAPI , HTTPException
from sqlalchemy.orm import Session
from .schemas import PatientResponse , PatientCreate , PatientUpdate

from .database import get_db
from .models import Patient


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