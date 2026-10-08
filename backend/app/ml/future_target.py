from datetime import datetime, timedelta


def find_future_glucose(
    readings,
    prediction_time,
    patient_id,
    horizon_hours=2,
    tolerance_minutes=10,
):
    target_time = prediction_time + timedelta(hours=horizon_hours)

    start_time = target_time - timedelta(minutes=tolerance_minutes)
    end_time = target_time + timedelta(minutes=tolerance_minutes)

    candidates = [
        reading
        for reading in readings
        if (
            reading["patient_id"] == patient_id
            and reading["timestamp"] > prediction_time
            and start_time <= reading["timestamp"] <= end_time
            and reading.get("glucose_level") is not None
        )
    ]

    if not candidates:
        return None

    closest = min(
        candidates,
        key=lambda reading: abs(
            reading["timestamp"] - target_time
        ),
    )

    return closest