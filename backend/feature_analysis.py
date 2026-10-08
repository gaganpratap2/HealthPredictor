import random
from datetime import datetime
from statistics import mean

from app.ml.synthetic_generator import generate_population
from app.ml.population_dataset import build_population_dataset
from app.ml.feature_engineering import build_feature_vector


rng = random.Random(42)

readings = generate_population(
    number_of_patients=10,
    start_time=datetime(2026, 1, 1),
    number_of_days=3,
    rng=rng,
)

dataset = build_population_dataset(readings)


spike_features = []
normal_features = []

for observation in dataset:
    features = build_feature_vector(observation)

    if observation["target_glucose_spike"] == 1:
        spike_features.append(features)
    else:
        normal_features.append(features)


feature_names = [
    "glucose",
    "heart_rate",
    "hrv",
    "spo2",
    "steps",
    "glucose_baseline",
    "glucose_delta",
    "meal_proximity_minutes",
]


print("SPIKE OBSERVATIONS:")
print(len(spike_features))
print()

print("NORMAL OBSERVATIONS:")
print(len(normal_features))
print()


for feature in feature_names:
    spike_values = [
        row[feature]
        for row in spike_features
        if row[feature] is not None
    ]

    normal_values = [
        row[feature]
        for row in normal_features
        if row[feature] is not None
    ]

    print(f"===== {feature} =====")

    print(
        "Spike mean:",
        round(mean(spike_values), 3)
    )

    print(
        "Normal mean:",
        round(mean(normal_values), 3)
    )

    print()