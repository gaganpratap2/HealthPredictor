import random
from datetime import datetime

from app.ml.synthetic_generator import generate_population
from app.ml.dataset_builder import build_prediction_observation
from app.ml.feature_engineering import build_feature_vector
from app.ml.dataset_matrix import build_matrix


rng = random.Random(42)

readings = generate_population(
    number_of_patients=5,
    start_time=datetime(2026, 1, 1),
    rng=rng,
)

dataset = []

for reading in readings:
    observation = build_prediction_observation(
        reading=reading,
        all_readings=readings,
    )

    if observation is not None:
        feature_vector = build_feature_vector(observation)

        feature_vector["target_glucose_spike"] = (
            observation["target_glucose_spike"]
        )

        dataset.append(feature_vector)


X, y = build_matrix(dataset)


print("Number of rows:")
print(len(X))

print("\nNumber of features:")
print(len(X[0]))

print("\nFirst X row:")
print(X[0])

print("\nFirst y value:")
print(y[0])

print("\nLast X row:")
print(X[-1])

print("\nLast y value:")
print(y[-1])