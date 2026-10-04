from fastapi import Depends, FastAPI , HTTPException
from sqlalchemy.orm import Session
from .schemas import CreateWearableEvent, GlucoseReadingResponse, PatientResponse , PatientCreate , PatientUpdate , CreateGlucoseReading , CreateClinicalRecord , ClinicalRecordResponse, WearableEventResponse 

from .database import get_db
from .models import ClinicalRecord, GlucoseReading, Patient , WearableEvent

from datetime import datetime
from app.services.twin_service import build_patient_twin

app = FastAPI()


@app.get("/")
def root():
    return {"message": "HealthPredictor API is running"}


@app.get("/health")
def health():
    return {"status": "healthy"}


@app.get("/patients" , response_model=list[PatientResponse]) 
#response_model=list[PatientResponse]: "The response should be a list of PatientResponse objects."
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





@app.post("/glucose-readings",response_model=GlucoseReadingResponse)
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


@app.post( "/clinical-records", response_model=ClinicalRecordResponse
)
def create_clinical_record(
    record: CreateClinicalRecord,
    db: Session = Depends(get_db)
):
    patient = db.query(Patient).filter(
        Patient.id == record.patient_id
    ).first()

    if patient is None:
        raise HTTPException(
            status_code=404,
            detail="Patient not found"
        )

    new_record = ClinicalRecord(
        patient_id=record.patient_id,
        record_type=record.record_type,
        description=record.description,
        record_date=record.record_date
    )

    db.add(new_record)
    db.commit()
    db.refresh(new_record)

    return new_record

@app.get("/patients/{patient_id}/clinical-records", response_model=list[ClinicalRecordResponse])
def get_patient_clinical_records(
    patient_id: int,
    db: Session = Depends(get_db)
):
    patient = db.query(Patient).filter(
        Patient.id == patient_id
    ).first()

    if patient is None:
        raise HTTPException(
            status_code=404,
            detail="Patient not found"
        )

    records = db.query(ClinicalRecord).filter(
        ClinicalRecord.patient_id == patient_id
    ).order_by(ClinicalRecord.record_date.desc()).all()

    return records



@app.post(
    "/wearable-events",
    response_model=WearableEventResponse
)
def create_wearable_event(
    event: CreateWearableEvent,
    db: Session = Depends(get_db)
):
    patient = db.query(Patient).filter(
        Patient.id == event.patient_id
    ).first()

    if patient is None:
        raise HTTPException(
            status_code=404,
            detail="Patient not found"
        )

    existing_event = db.query(WearableEvent).filter(
        WearableEvent.event_id == event.event_id
    ).first()

    if existing_event is not None:
        return existing_event

    new_event = WearableEvent(
        patient_id=event.patient_id,
        event_id=event.event_id,
        timestamp=event.timestamp,
        heart_rate=event.heart_rate,
        hrv=event.hrv,
        spo2=event.spo2,
        glucose_level=event.glucose_level,
        steps=event.steps,
        sleep_state=event.sleep_state,
        activity_state=event.activity_state,
        source=event.source
    )

    db.add(new_event)
    db.commit()
    db.refresh(new_event)

    return new_event

@app.get("/patients/{patient_id}/wearable-events",response_model=list[WearableEventResponse]
)
def get_patient_wearable_events(
    patient_id: int,
    db: Session = Depends(get_db)
):
    patient = db.query(Patient).filter(
        Patient.id == patient_id
    ).first()

    if patient is None:
        raise HTTPException(
            status_code=404,
            detail="Patient not found"
        )

    
    events = db.query(WearableEvent).filter(
        WearableEvent.patient_id == patient_id
    ).order_by(
        WearableEvent.timestamp.desc()
    ).all()

    return events



@app.get("/patients/{patient_id}/twin")
def get_patient_twin(
    patient_id: int,
    db: Session = Depends(get_db)
):
    twin = build_patient_twin(
        db=db,
        patient_id=patient_id,
        current_time=datetime.now(),
        window_minutes=60,
    )

    if twin is None:
        raise HTTPException(
            status_code=404,
            detail="No recent wearable data found"
        )

    return twin