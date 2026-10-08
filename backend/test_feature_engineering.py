import random
from datetime import datetime

from app.ml.synthetic_generator import generate_population
from app.ml.dataset_builder import build_prediction_observation
from app.ml.feature_engineering import build_feature_vector


rng = random.Random(42)

readings = generate_population(
    number_of_patients=5,
    start_time=datetime(2026,1,1),
    rng=rng,
)

dataset = []

for reading in readings:

    observation = build_prediction_observation(
        reading=reading,
        all_readings=readings,
    )

    if observation:
        dataset.append(observation)

features = [
    build_feature_vector(obs)
    for obs in dataset
]

print("Feature rows:")
print(len(features))

print("\nFirst feature vector:")
print(features[0])

print("\nLast feature vector:")
print(features[-1])