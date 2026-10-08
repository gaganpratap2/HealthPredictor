from datetime import datetime

from app.ml.future_target import find_future_glucose


readings = [
    {
        "timestamp": datetime.fromisoformat(
            "2026-10-05T10:00:00"
        ),
        "glucose_level": 105.0,
    },
    {
        "timestamp": datetime.fromisoformat(
            "2026-10-05T11:55:00"
        ),
        "glucose_level": 138.0,
    },
    {
        "timestamp": datetime.fromisoformat(
            "2026-10-05T12:03:00"
        ),
        "glucose_level": 145.0,
    },
    {
        "timestamp": datetime.fromisoformat(
            "2026-10-05T12:20:00"
        ),
        "glucose_level": 155.0,
    },
]


prediction_time = datetime.fromisoformat(
    "2026-10-05T10:00:00"
)

future = find_future_glucose(
    readings=readings,
    prediction_time=prediction_time,
)

print("Future observation:")
print(future)