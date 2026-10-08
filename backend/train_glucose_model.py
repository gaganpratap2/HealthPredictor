import random
from datetime import datetime

from app.ml.synthetic_generator import generate_population
from app.ml.population_dataset import build_population_dataset
from app.ml.dataset_split import split_by_patient
from app.ml.feature_engineering import build_feature_vector
from app.ml.dataset_matrix import build_matrix
from app.ml.preprocessing import (
    fit_scaler,
    transform_features,
)
from app.ml.train import train_logistic_regression
from app.ml.evaluation import evaluate_classifier

from app.ml.error_analysis import analyze_predictions
rng = random.Random(42)


# ---------------------------------
# 1. Generate larger population
# ---------------------------------

readings = generate_population(
    number_of_patients=10,
    start_time=datetime(2026, 1, 1),
    number_of_days=3,
    rng=rng,
)


# ---------------------------------
# 2. Build labeled dataset
# ---------------------------------

dataset = build_population_dataset(readings)


print("Raw readings:")
print(len(readings))

print()

print("Labeled observations:")
print(len(dataset))

print()


# ---------------------------------
# 3. Patient-level split
# ---------------------------------

train, validation, test = split_by_patient(
    dataset=dataset,
    train_patients=[1, 2, 3, 4, 5, 6],
    validation_patients=[7, 8],
    test_patients=[9, 10],
)


print("Train observations:")
print(len(train))

print()

print("Validation observations:")
print(len(validation))

print()

print("Test observations:")
print(len(test))

print()


# ---------------------------------
# 4. Build feature matrices
# ---------------------------------

def prepare_matrix(dataset):
    feature_rows = []

    sorted_dataset = sorted(
        dataset,
        key=lambda observation: (
            observation["patient_id"],
            observation["timestamp"],
        )
    )

    previous_by_patient = {}

    for observation in sorted_dataset:
        patient_id = observation["patient_id"]

        previous_observation = previous_by_patient.get(
            patient_id
        )

        features = build_feature_vector(
            observation,
            previous_observation=previous_observation,
        )

        if features["glucose_rate"] is None:
            previous_by_patient[patient_id] = observation
            continue

        features["target_glucose_spike"] = (
            observation["target_glucose_spike"]
        )

        feature_rows.append(features)

        previous_by_patient[patient_id] = observation

    return build_matrix(feature_rows)


X_train, y_train = prepare_matrix(train)
X_validation, y_validation = prepare_matrix(validation)
X_test, y_test = prepare_matrix(test)


# ---------------------------------
# 5. Fit scaler ONLY on training data
# ---------------------------------

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


# ---------------------------------
# 6. Train baseline model
# ---------------------------------

model = train_logistic_regression(
    X_train=X_train_scaled,
    y_train=y_train,
)


# ---------------------------------
# 7. Predictions
# ---------------------------------

train_predictions = model.predict(
    X_train_scaled
)

validation_predictions = model.predict(
    X_validation_scaled
)

test_predictions = model.predict(
    X_test_scaled
)


train_probabilities = (
    model.predict_proba(X_train_scaled)[:, 1]
)

validation_probabilities = (
    model.predict_proba(X_validation_scaled)[:, 1]
)

test_probabilities = (
    model.predict_proba(X_test_scaled)[:, 1]
)


# ---------------------------------
# 8. Evaluation
# ---------------------------------

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


false_positives, false_negatives = analyze_predictions(
    dataset=test,
    predictions=test_predictions,
    probabilities=test_probabilities,
)

print()
print("====== ERROR ANALYSIS ======")
print("False positives:", len(false_positives))
print("False negatives:", len(false_negatives))

print()
print("First 10 false positives:")

for item in false_positives[:10]:
    print(item)

print()
print("First 10 false negatives:")

for item in false_negatives[:10]:
    print(item)



print("========== TRAIN ==========")
print(train_metrics)

print()

print("====== VALIDATION ======")
print(validation_metrics)

print()

print("========== TEST ==========")
print(test_metrics)