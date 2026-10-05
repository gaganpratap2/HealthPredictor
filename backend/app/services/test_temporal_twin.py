from datetime import datetime, timedelta
import uuid
from app.database import SessionLocal
from app.models import WearableEvent
from app.services.twin_service import build_patient_twin


db = SessionLocal()

start_time = datetime.fromisoformat(
    "2026-10-05T10:00:00"
)

values = [
    (105, 70, 50, 98),
    (108, 73, 48, 98),
    (114, 78, 45, 97),
    (123, 84, 42, 97),
    (132, 89, 39, 97),
]

run_id = uuid.uuid4().hex[:8]

for index, (glucose, heart_rate, hrv, spo2) in enumerate(values):
    event = WearableEvent(
        patient_id=1,
        event_id=f"DAY8-{run_id}-{index + 1}",
        timestamp=start_time + timedelta(minutes=index * 5),
        glucose_level=glucose,
        heart_rate=heart_rate,
        hrv=hrv,
        spo2=spo2,
        steps=10 + index * 5,
        activity_state="walking",
        sleep_state="awake",
        source="day8-test",
    )

    db.add(event)

db.commit()

twin = build_patient_twin(
    db=db,
    patient_id=1,
    current_time=datetime.fromisoformat(
        "2026-10-05T10:20:00"
    ),
    window_minutes=60,
)

print("\nTEMPORAL DIGITAL TWIN")
print(twin["temporal_state"])

db.close()