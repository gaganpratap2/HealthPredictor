import random
from datetime import datetime

from app.ml.synthetic_generator import generate_population
from app.ml.population_dataset import build_population_dataset


rng = random.Random(42)

readings = generate_population(
    number_of_patients=10,
    start_time=datetime(2026, 1, 1),
    number_of_days=3,
    rng=rng,
)

dataset = build_population_dataset(readings)

print("Raw readings:")
print(len(readings))

print()

print("Dataset observations:")
print(len(dataset))

print()

patient_ids = sorted(
    set(
        observation["patient_id"]
        for observation in dataset
    )
)

print("Patients in dataset:")
print(patient_ids)

print()

spikes = sum(
    observation["target_glucose_spike"]
    for observation in dataset
)

print("Spike observations:")
print(spikes)

print()

print("Normal observations:")
print(len(dataset) - spikes)