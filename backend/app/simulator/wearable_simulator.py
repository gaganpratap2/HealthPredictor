import random
from datetime import datetime, timedelta
import uuid

patient_id = 1
start_time = datetime.now()

activities = [
    "resting",
    "resting",
    "walking",
    "walking",
    "walking",
    "recovery",
    "resting",
    "resting",
    "walking",
    "recovery"
]

for i, activity in enumerate(activities):

    # -----------------------------
    # Activity-based baseline
    # -----------------------------
    if activity == "resting":
        base_heart_rate = 70
        base_hrv = 45
        base_steps = 0

    elif activity == "walking":
        base_heart_rate = 85
        base_hrv = 35
        base_steps = 50

    else:
        base_heart_rate = 75
        base_hrv = 40
        base_steps = 20

    # -----------------------------
    # Heart Rate
    # -----------------------------
    heart_rate = base_heart_rate + random.uniform(-2, 2)

    if random.random() < 0.1:
        heart_rate = None

    # -----------------------------
    # HRV
    # -----------------------------
    hrv = base_hrv + random.uniform(-2, 2)

    if random.random() < 0.1:
        hrv = None

    # -----------------------------
    # SpO2
    # -----------------------------
    spo2 = 98 + random.uniform(-0.5, 0.5)

    if random.random() < 0.1:
        spo2 = None

    # -----------------------------
    # Steps
    # -----------------------------
    steps = max(
        0,
        int(base_steps + random.uniform(-5, 5))
    )

    if random.random() < 0.1:
        steps = None

    # -----------------------------
    # Glucose
    # -----------------------------
    if i < 3:
        glucose_level = 110 + random.uniform(-2, 2)

    elif i < 6:
        glucose_level = (
            110
            + (i - 2) * 8
            + random.uniform(-2, 2)
        )

    elif i < 9:
        glucose_level = 135 + random.uniform(-3, 3)

    else:
        glucose_level = (
            135
            - (i - 8) * 6
            + random.uniform(-2, 2)
        )

    if random.random() < 0.1:
        glucose_level = None

    # -----------------------------
    # Create event
    # -----------------------------
    event = {
        "patient_id": patient_id,
        "event_id": f"SIM-{uuid.uuid4()}",
        "timestamp": start_time.isoformat(),

        "heart_rate": (
            round(heart_rate, 2)
            if heart_rate is not None
            else None
        ),

        "hrv": (
            round(hrv, 2)
            if hrv is not None
            else None
        ),

        "spo2": (
            round(spo2, 2)
            if spo2 is not None
            else None
        ),

        "glucose_level": (
            round(glucose_level, 2)
            if glucose_level is not None
            else None
        ),

        "steps": steps,

        "sleep_state": "awake",
        "activity_state": activity,
        "source": "synthetic_sensor"
    }

    print(event)

    # Move to next minute
    start_time += timedelta(minutes=1)
