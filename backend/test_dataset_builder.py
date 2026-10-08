import random
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


print("Raw readings:")
print(len(readings))

print("\nLabeled observations:")
print(len(dataset))

print("\nFirst observation:")
print(dataset[0])

print("\nLast observation:")
print(dataset[-1])