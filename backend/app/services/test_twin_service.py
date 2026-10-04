from datetime import datetime
from app.database import SessionLocal
from app.services.twin_service import calculate_patient_features


db = SessionLocal()

try:
    features = calculate_patient_features(
        db=db,
        patient_id=1,
        current_time=datetime.now(),
        window_minutes=60
    )

    print("\nPatient Features:")
    print(features)

finally:
    db.close()
