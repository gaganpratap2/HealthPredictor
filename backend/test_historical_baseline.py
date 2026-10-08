from datetime import datetime

from app.ml.historical_baseline import calculate_historical_baseline


readings = [
    {
        "timestamp": datetime.fromisoformat(
            "2026-10-05T09:00:00"
        ),
        "glucose_level": 100.0,
    },
    {
        "timestamp": datetime.fromisoformat(
            "2026-10-05T09:30:00"
        ),
        "glucose_level": 110.0,
    },
    {
        "timestamp": datetime.fromisoformat(
            "2026-10-05T10:00:00"
        ),
        "glucose_level": 120.0,
    },
    {
        "timestamp": datetime.fromisoformat(
            "2026-10-05T12:00:00"
        ),
        "glucose_level": 150.0,
    },
]


prediction_time = datetime.fromisoformat(
    "2026-10-05T10:00:00"
)

baseline = calculate_historical_baseline(
    readings=readings,
    prediction_time=prediction_time,
)

print("Historical baseline:", baseline)