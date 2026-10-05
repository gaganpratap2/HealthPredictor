from datetime import datetime

from app.services.time_features import (
    calculate_temporal_features,
)


readings = [
    {
        "timestamp": datetime.fromisoformat("2026-10-05T10:00:00"),
        "glucose_level": 100,
        "heart_rate": 70,
        "hrv": 50,
        "spo2": 98,
    },
    {
        "timestamp": datetime.fromisoformat("2026-10-05T10:05:00"),
        "glucose_level": 105,
        "heart_rate": 75,
        "hrv": 48,
        "spo2": 98,
    },
    {
        "timestamp": datetime.fromisoformat("2026-10-05T10:10:00"),
        "glucose_level": 115,
        "heart_rate": 82,
        "hrv": 45,
        "spo2": 97,
    },
    {
        "timestamp": datetime.fromisoformat("2026-10-05T10:15:00"),
        "glucose_level": 130,
        "heart_rate": 90,
        "hrv": 40,
        "spo2": 97,
    },
]

signals = [
    "glucose_level",
    "heart_rate",
    "hrv",
    "spo2",
]


current_time = datetime.fromisoformat(
    "2026-10-05T10:15:00"
)


features = calculate_temporal_features(
    readings,
    "glucose_level",
    current_time,
) 
for signal in signals:
    features = calculate_temporal_features(
        readings,
        signal,
        current_time,
    )

    print(f"\n{signal}")
    print(features)




print("TEMPORAL FEATURES")
print(features)