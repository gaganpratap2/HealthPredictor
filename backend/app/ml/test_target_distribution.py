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


targets = [
    observation["target_glucose_spike"]
    for observation in dataset
]

target_counts = Counter(targets)

patient_counts = Counter(
    observation["patient_id"]
    for observation in dataset
)


print("Total labeled observations:")
print(len(dataset))

print("\nTarget distribution:")
print(target_counts)

print("\nNormal examples:")
print(target_counts[0])

print("\nSpike examples:")
print(target_counts[1])

spike_percentage = (
    target_counts[1] / len(dataset)
) * 100

print("\nSpike percentage:")
print(round(spike_percentage, 2), "%")

print("\nPatients:")
print(len(patient_counts))

print("\nObservations per patient:")

for patient_id, count in sorted(patient_counts.items()):
    print(
        f"Patient {patient_id}: {count}"
    )