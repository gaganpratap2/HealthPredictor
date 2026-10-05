from sqlalchemy.orm import Session

from app.models import WearableEvent


def get_patient_timeline(
    db: Session,
    patient_id: int,
):
    events = (
        db.query(WearableEvent)
        .filter(
            WearableEvent.patient_id == patient_id
        )
        .order_by(
            WearableEvent.timestamp.asc()
        )
        .all()
    )

    timeline = []

    for event in events:
        timeline.append({
            "event_type": "wearable",
            "event_id": event.event_id,
            "timestamp": event.timestamp,
            "glucose": event.glucose_level,
            "heart_rate": event.heart_rate,
            "hrv": event.hrv,
            "spo2": event.spo2,
            "activity_state": event.activity_state,
            "sleep_state": event.sleep_state,
        })

    return timeline