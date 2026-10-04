from datetime import datetime

from app.database import SessionLocal
from app.services.twin_service import build_patient_twin


db = SessionLocal()

try:
    twin = build_patient_twin(
        db=db,
        patient_id=1,
        current_time=datetime.fromisoformat(
        "2026-10-02T10:20:00"
        ),
        window_minutes=60,
    )

    print("\nDIGITAL TWIN")
    print(twin)

finally:
    db.close()