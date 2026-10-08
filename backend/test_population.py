import random
from datetime import datetime

from app.ml.synthetic_generator import generate_population


rng = random.Random(42)

readings = generate_population(
    number_of_patients=10,
    start_time=datetime(2026, 1, 1),
    number_of_days=3,
    rng=rng,
)

print("Total readings:")
print(len(readings))

print()

print("Patients:")

patient_ids = sorted(
    set(
        reading["patient_id"]
        for reading in readings
    )
)

print(patient_ids)