import random
from datetime import datetime

from app.ml.synthetic_generator import generate_population
from app.ml.dataset_builder import build_prediction_observation
from app.ml.dataset_split import split_by_patient
from app.ml.feature_engineering import build_feature_vector
from app.ml.dataset_matrix import build_matrix
from app.ml.preprocessing import (
    fit_scaler,
    transform_features,
)
from app.ml.train import train_logistic_regression
from app.ml.evaluation import evaluate_classifier

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


train, validation, test = split_by_patient(
    dataset=dataset,
    train_patients=[1, 2, 3],
    validation_patients=[4],
    test_patients=[5],
)


def prepare_matrix(dataset):
    feature_rows = []

    for observation in dataset:
        features = build_feature_vector(
            observation
        )

        features["target_glucose_spike"] = (
            observation["target_glucose_spike"]
        )

        feature_rows.append(features)

    return build_matrix(feature_rows)


X_train, y_train = prepare_matrix(train)
X_validation, y_validation = prepare_matrix(validation)
X_test, y_test = prepare_matrix(test)


scaler = fit_scaler(X_train)

X_train_scaled = transform_features(
    scaler,
    X_train,
)

X_validation_scaled = transform_features(
    scaler,
    X_validation,
)

X_test_scaled = transform_features(
    scaler,
    X_test,
)


model = train_logistic_regression(
    X_train=X_train_scaled,
    y_train=y_train,
)


train_predictions = model.predict(
    X_train_scaled
)



validation_predictions = model.predict(
    X_validation_scaled
)

test_predictions = model.predict(
    X_test_scaled
)


train_probabilities = model.predict_proba(
    X_train_scaled
)[:, 1]

validation_probabilities = model.predict_proba(
    X_validation_scaled
)[:, 1]

test_probabilities = model.predict_proba(
    X_test_scaled
)[:, 1]


train_metrics = evaluate_classifier(
    y_true=y_train,
    predictions=train_predictions,
    probabilities=train_probabilities,
)

validation_metrics = evaluate_classifier(
    y_true=y_validation,
    predictions=validation_predictions,
    probabilities=validation_probabilities,
)

test_metrics = evaluate_classifier(
    y_true=y_test,
    predictions=test_predictions,
    probabilities=test_probabilities,
)


print("Model trained successfully")
print()

print("Train predictions:")
print(train_predictions[:20])

print()

print("Validation predictions:")
print(validation_predictions[:20])

print()

print("Test predictions:")
print(test_predictions[:20])


print()
print("TRAIN METRICS")
print(train_metrics)

print()
print("VALIDATION METRICS")
print(validation_metrics)

print()
print("TEST METRICS")
print(test_metrics)