import random
from datetime import datetime

from app.ml.synthetic_generator import (
    generate_patient_profile,
    generate_patient_history,
)


rng = random.Random(42)

patient = generate_patient_profile(
    patient_id=1,
    rng=rng,
)

readings = generate_patient_history(
    patient=patient,
    start_time=datetime(2026, 1, 1),
    number_of_days=3,
    rng=rng,
)

print("Number of readings:")
print(len(readings))

print()

print("First reading:")
print(readings[0])

print()

print("Last reading:")
print(readings[-1])