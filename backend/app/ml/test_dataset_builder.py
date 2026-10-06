from datetime import datetime

from app.ml.dataset_builder import build_prediction_observation


readings = [
    {
        "patient_id": 1,
        "timestamp": datetime.fromisoformat(
            "2026-10-05T09:00:00"
        ),
        "glucose_level": 100.0,
        "heart_rate": 72.0,
        "hrv": 50.0,
        "spo2": 98.0,
        "steps": 50,
    },
    {
        "patient_id": 1,
        "timestamp": datetime.fromisoformat(
            "2026-10-05T09:30:00"
        ),
        "glucose_level": 110.0,
        "heart_rate": 74.0,
        "hrv": 48.0,
        "spo2": 98.0,
        "steps": 80,
    },
    {
        "patient_id": 1,
        "timestamp": datetime.fromisoformat(
            "2026-10-05T10:00:00"
        ),
        "glucose_level": 120.0,
        "heart_rate": 78.0,
        "hrv": 45.0,
        "spo2": 98.0,
        "steps": 100,
    },
    {
        "patient_id": 1,
        "timestamp": datetime.fromisoformat(
            "2026-10-05T12:03:00"
        ),
        "glucose_level": 150.0,
        "heart_rate": 82.0,
        "hrv": 42.0,
        "spo2": 97.0,
        "steps": 500,
    },
]


observation = build_prediction_observation(
    reading=readings[2],
    all_readings=readings,
)

print("PREDICTION OBSERVATION")
print(observation)