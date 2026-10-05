from app.database import SessionLocal
from app.services.timeline_service import get_patient_timeline


db = SessionLocal()

timeline = get_patient_timeline(
    db=db,
    patient_id=1,
)

print("\nPATIENT TIMELINE")

for event in timeline:
    print(event)

db.close()