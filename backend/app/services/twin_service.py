from datetime import datetime, timedelta

from sqlalchemy.orm import Session

from app.models import WearableEvent
from app.services.data_quality import calculate_data_quality
from app.services.digital_twin import build_twin_state
from app.services.event_adapter import wearable_event_to_dict
from app.services.time_features import (
    calculate_baseline_stats,
    calculate_current_values,
    calculate_multi_signal_features,
)


def get_recent_events(
    db: Session,
    patient_id: int,
    current_time: datetime,
    minutes: int,
):
    start_time = current_time - timedelta(minutes=minutes)

    events = (
        db.query(WearableEvent)
        .filter(
            WearableEvent.patient_id == patient_id,
            WearableEvent.timestamp >= start_time,
            WearableEvent.timestamp <= current_time,
        )
        .order_by(WearableEvent.timestamp.asc())
        .all()
    )

    return [
        wearable_event_to_dict(event)
        for event in events
    ]


def calculate_patient_features(
    db: Session,
    patient_id: int,
    current_time: datetime,
    window_minutes: int = 5,
):
    readings = get_recent_events(
        db,
        patient_id,
        current_time,
        window_minutes,
    )

    if not readings:
        return {}

    return calculate_multi_signal_features(readings)


def get_historical_glucose(
    db: Session,
    patient_id: int,
):
    events = (
        db.query(WearableEvent)
        .filter(
            WearableEvent.patient_id == patient_id,
            WearableEvent.glucose_level.isnot(None),
        )
        .order_by(WearableEvent.timestamp.asc())
        .all()
    )

    return [
        event.glucose_level
        for event in events
    ]


def build_patient_twin(
    db: Session,
    patient_id: int,
    current_time: datetime,
    window_minutes: int = 60,
):
    readings = get_recent_events(
        db,
        patient_id,
        current_time,
        window_minutes,
    )

    if not readings:
        return None

    features = calculate_multi_signal_features(readings)

    current_values = calculate_current_values(readings)

    data_quality = calculate_data_quality(readings)

    historical_glucose = get_historical_glucose(
        db,
        patient_id,
    )

    baseline = calculate_baseline_stats(
        historical_glucose
    )

    return build_twin_state(
        patient_id=patient_id,
        features=features,
        current_values=current_values,
        baseline_mean=baseline.get("mean"),
        baseline_std=baseline.get("std"),
        data_quality=data_quality,
        readings=readings,
        current_time=current_time,
)