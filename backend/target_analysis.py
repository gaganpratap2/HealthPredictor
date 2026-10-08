import random
from datetime import datetime
from collections import Counter

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


spikes = []


def meal_window(timestamp):
    hour = timestamp.hour

    if 8 <= hour < 10:
        return "breakfast_window"

    if 13 <= hour < 15:
        return "lunch_window"

    if 19 <= hour < 21:
        return "dinner_window"

    return "outside_meal_window"


print("TOTAL SPIKES:")
print(len(spikes))
print()

print("SPIKES BY TIME WINDOW:")

from app.ml.future_target import find_future_glucose


spikes = []

for observation in dataset:
    if observation["target_glucose_spike"] != 1:
        continue

    future = find_future_glucose(
        readings=readings,
        prediction_time=observation["timestamp"],
        patient_id=observation["patient_id"],
    )

    if future is not None:
        spikes.append(future)


counter = Counter(
    meal_window(observation["timestamp"])
    for observation in spikes
)