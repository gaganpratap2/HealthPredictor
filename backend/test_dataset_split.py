import random
from datetime import datetime

from app.ml.synthetic_generator import generate_population
from app.ml.dataset_builder import build_prediction_observation
from app.ml.feature_engineering import build_feature_vector
from app.ml.dataset_split import split_by_patient


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

        feature_vector["patient_id"] = (
            observation["patient_id"]
        )

        feature_vector["target_glucose_spike"] = (
            observation["target_glucose_spike"]
        )

        dataset.append(feature_vector)


train, validation, test = split_by_patient(
    dataset=dataset,
    train_patients=[1, 2, 3],
    validation_patients=[4],
    test_patients=[5],
)


def get_patient_ids(data):
    return sorted(
        set(
            observation["patient_id"]
            for observation in data
        )
    )


print("Train:")
print(len(train))
print(get_patient_ids(train))

print("\nValidation:")
print(len(validation))
print(get_patient_ids(validation))

print("\nTest:")
print(len(test))
print(get_patient_ids(test))