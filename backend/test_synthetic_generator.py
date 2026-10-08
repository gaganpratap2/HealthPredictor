import random
from datetime import datetime

from app.ml.synthetic_generator import generate_population


rng = random.Random(42)

readings = generate_population(
    number_of_patients=5,
    start_time=datetime(2026, 1, 1, 0, 0),
    rng=rng,
)

print("Total readings:")
print(len(readings))

patient_ids = sorted(
    set(reading["patient_id"] for reading in readings)
)

print("\nPatients:")
print(patient_ids)

for patient_id in patient_ids:
    patient_readings = [
        reading
        for reading in readings
        if reading["patient_id"] == patient_id
    ]

    print(
        f"Patient {patient_id}: "
        f"{len(patient_readings)} readings"
    )

print("\nFirst reading:")
print(readings[0])

print("\nLast reading:")
print(readings[-1])