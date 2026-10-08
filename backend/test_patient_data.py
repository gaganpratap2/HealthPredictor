import random
from datetime import datetime

from app.ml.synthetic_generator import generate_population
from app.ml.patient_data import group_readings_by_patient


rng = random.Random(42)

readings = generate_population(
    number_of_patients=10,
    start_time=datetime(2026, 1, 1),
    number_of_days=3,
    rng=rng,
)

grouped = group_readings_by_patient(readings)

print("Total readings:")
print(len(readings))

print()

print("Number of patients:")
print(len(grouped))

print()

for patient_id, patient_readings in grouped.items():
    print(
        f"Patient {patient_id}: "
        f"{len(patient_readings)} readings"
    )