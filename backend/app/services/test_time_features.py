from datetime import datetime

from time_features import calculate_multi_signal_features , get_recent_readings


readings = [
    {
        "timestamp": datetime(2026, 10, 3, 10, 0),
        "glucose_level": 110,
        "heart_rate": 70,
        "hrv": 45,
        "spo2": 98,
        "steps": 0,
    },
    {
        "timestamp": datetime(2026, 10, 3, 10, 1),
        "glucose_level": 115,
        "heart_rate": 78,
        "hrv": 42,
        "spo2": 98,
        "steps": 40,
    },
    {
        "timestamp": datetime(2026, 10, 3, 10, 2),
        "glucose_level": 125,
        "heart_rate": 84,
        "hrv": None,
        "spo2": 97,
        "steps": 50,
    },
    {
        "timestamp": datetime(2026, 10, 3, 10, 3),
        "glucose_level": 135,
        "heart_rate": 88,
        "hrv": 35,
        "spo2": 97,
        "steps": 60,
    },
]

current_time = datetime(2026, 10, 3, 10, 5)

recent = get_recent_readings(
    readings,
    current_time,
    5
)

features = calculate_multi_signal_features(recent)

for reading in recent:
    print(features)