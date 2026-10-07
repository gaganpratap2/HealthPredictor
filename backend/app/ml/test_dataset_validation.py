import random
from collections import Counter
from datetime import datetime

from app.ml.synthetic_generator import generate_population
from app.ml.dataset_builder import build_prediction_observation


rng = random.Random(42)

readings = generate_population(
    number_of_patients=5,
    start_time=datetime(2026, 1, 1, 0, 0),
    rng=rng,
)


dataset = []

for reading in readings:
    observation = build_prediction_observation(
        reading=reading,
        all_readings=readings,
    )

    if observation is not None:
        dataset.append(observation)


print("Total observations:")
print(len(dataset))


# 1. Check duplicate patient/timestamp pairs

keys = [
    (
        observation["patient_id"],
        observation["timestamp"],
    )
    for observation in dataset
]

duplicate_count = len(keys) - len(set(keys))

print("\nDuplicate prediction timestamps:")
print(duplicate_count)


# 2. Check future target exists

missing_targets = sum(
    observation["target_future_glucose"] is None
    for observation in dataset
)

print("\nMissing future targets:")
print(missing_targets)


# 3. Check target class values

target_values = Counter(
    observation["target_glucose_spike"]
    for observation in dataset
)

print("\nTarget values:")
print(target_values)


# 4. Print representative examples

print("\nSample observations:")

for observation in dataset[:5]:
    print(
        observation["patient_id"],
        observation["timestamp"],
        "current=",
        observation["glucose"],
        "baseline=",
        round(observation["glucose_baseline"], 2),
        "future=",
        observation["target_future_glucose"],
        "target=",
        observation["target_glucose_spike"],
    )