
import random
from datetime import datetime
from app.ml.threshold_analysis import analyze_thresholds
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

from app.ml.feature_analysis import analyze_logistic_coefficients
from app.ml.dataset_matrix import FEATURE_NAMES
# ---------------------------------
# 1. Generate synthetic population
# ---------------------------------

rng = random.Random(42)

readings = generate_population(
    number_of_patients=10,
    start_time=datetime(2026, 1, 1),
    number_of_days=3,
    rng=rng,
)

print("Raw readings:", len(readings))


# ---------------------------------
# 2. Build labeled dataset
# ---------------------------------

dataset = build_population_dataset(readings)

print("Labeled observations:", len(dataset))


# ---------------------------------
# 3. Split by patient
# ---------------------------------

train, validation, test = split_by_patient(
    dataset=dataset,
    train_patients=[1, 2, 3, 4, 5, 6],
    validation_patients=[7, 8],
    test_patients=[9, 10],
)

print("Train observations:", len(train))
print("Validation observations:", len(validation))
print("Test observations:", len(test))


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
        ),
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

        # Update the previous observation for the next reading.
        previous_by_patient[patient_id] = observation

        # A glucose rate cannot be calculated without a
        # previous observation.
        if features["glucose_rate"] is None:
            continue

        # Keep metadata for error analysis.
        # These fields are NOT model inputs.
        features["patient_id"] = patient_id
        features["timestamp"] = observation["timestamp"]
        features["target_glucose_spike"] = (
            observation["target_glucose_spike"]
        )

        feature_rows.append(features)

    X, y = build_matrix(feature_rows)

    # Verify that rows and labels remain aligned.
    assert len(X) == len(y) == len(feature_rows)

    return X, y, feature_rows


X_train, y_train, train_rows = prepare_matrix(train)

X_validation, y_validation, validation_rows = (
    prepare_matrix(validation)
)

X_test, y_test, test_rows = prepare_matrix(test)

print()
print("Prepared training rows:", len(train_rows))
print("Prepared validation rows:", len(validation_rows))
print("Prepared test rows:", len(test_rows))


# ---------------------------------
# 5. Fit scaler on training data only
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

analyze_logistic_coefficients(
    model=model,
    feature_names=FEATURE_NAMES,
)
# ---------------------------------
# 7. Generate predictions
# ---------------------------------

train_predictions = model.predict(X_train_scaled)

validation_predictions = model.predict(
    X_validation_scaled
)

test_predictions = model.predict(X_test_scaled)




# Probability that each observation belongs to class 1.
train_probabilities = model.predict_proba(
    X_train_scaled
)[:, 1]

validation_probabilities = model.predict_proba(
    X_validation_scaled
)[:, 1]

test_probabilities = model.predict_proba(
    X_test_scaled
)[:, 1]

analyze_thresholds(
    y_true=y_validation,
    probabilities=validation_probabilities,
)



# ---------------------------------
# Evaluate selected threshold
# ---------------------------------

SELECTED_THRESHOLD = 0.80

test_predictions_at_threshold = [
    int(probability >= SELECTED_THRESHOLD)
    for probability in test_probabilities
]

threshold_test_metrics = evaluate_classifier(
    y_true=y_test,
    predictions=test_predictions_at_threshold,
    probabilities=test_probabilities,
)

print()
print("====== TEST: THRESHOLD 0.80 ======")
print(threshold_test_metrics)



# ---------------------------------
# 8. Verify test prediction alignment
# ---------------------------------

assert len(test_rows) == len(y_test)
assert len(test_rows) == len(test_predictions)
assert len(test_rows) == len(test_probabilities)


# ---------------------------------
# 9. Evaluate the model
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


# ---------------------------------
# 10. Analyze real test errors
# ---------------------------------


false_positives, false_negatives = analyze_predictions(
    dataset=test_rows,
    predictions=test_predictions_at_threshold,
    probabilities=test_probabilities,
)


print()
print("========== ERROR ANALYSIS ==========")
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


# ---------------------------------
# 11. Print evaluation metrics
# ---------------------------------

print()
print("========== TRAIN ==========")
print(train_metrics)

print()
print("====== VALIDATION ======")
print(validation_metrics)

print()
print("========== TEST ==========")
print(test_metrics)
