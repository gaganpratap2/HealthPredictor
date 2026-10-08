from collections import Counter

from app.ml.synthetic_generator import generate_population
from app.ml.population_dataset import build_population_dataset

import random
from datetime import datetime


rng = random.Random(42)

readings = generate_population(
    number_of_patients=10,
    start_time=datetime(2026, 1, 1),
    number_of_days=3,
    rng=rng,
)

dataset = build_population_dataset(readings)


# 1. Check duplicate timestamps per patient

keys = [
    (
        observation["patient_id"],
        observation["timestamp"],
    )
    for observation in dataset
]

counts = Counter(keys)

duplicates = [
    key
    for key, count in counts.items()
    if count > 1
]


# 2. Check missing future targets

missing_future = [
    observation
    for observation in dataset
    if observation["target_future_glucose"] is None
]


# 3. Check missing spike labels

missing_labels = [
    observation
    for observation in dataset
    if observation["target_glucose_spike"] is None
]


print("Dataset size:")
print(len(dataset))

print()

print("Duplicate patient/timestamp pairs:")
print(len(duplicates))

print()

print("Missing future targets:")
print(len(missing_future))

print()

print("Missing spike labels:")
print(len(missing_labels))