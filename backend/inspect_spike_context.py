import random
from datetime import datetime

from app.ml.synthetic_generator import generate_population
from app.ml.population_dataset import build_population_dataset
from app.ml.future_target import find_future_glucose


rng = random.Random(42)

readings = generate_population(
    number_of_patients=10,
    start_time=datetime(2026, 1, 1),
    number_of_days=3,
    rng=rng,
)

dataset = build_population_dataset(readings)

spikes = [
    observation
    for observation in dataset
    if observation["target_glucose_spike"] == 1
]


print("TOTAL SPIKES:")
print(len(spikes))
print()

print("FIRST 10 SPIKE CONTEXTS:")
print()

for observation in spikes[:10]:

    future = find_future_glucose(
        readings=readings,
        prediction_time=observation["timestamp"],
        patient_id=observation["patient_id"],
    )

    if future is None:
        continue

    print(
        "Patient:",
        observation["patient_id"]
    )

    print(
        "Prediction:",
        observation["timestamp"]
    )

    print(
        "Current glucose:",
        observation["glucose"]
    )

    print(
        "Future:",
        future["timestamp"]
    )

    print(
        "Future glucose:",
        future["glucose_level"]
    )

    print(
        "Future hour:",
        future["timestamp"].hour
    )

    print("-" * 40)