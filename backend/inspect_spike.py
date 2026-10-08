import random
from datetime import datetime

from app.ml.synthetic_generator import generate_population
from app.ml.population_dataset import build_population_dataset
from app.ml.historical_baseline import calculate_historical_baseline
from app.ml.future_target import find_future_glucose


rng = random.Random(42)

readings = generate_population(
    number_of_patients=10,
    start_time=datetime(2026, 1, 1),
    number_of_days=3,
    rng=rng,
)

dataset = build_population_dataset(readings)

spike = next(
    observation
    for observation in dataset
    if observation["target_glucose_spike"] == 1
)

patient_id = spike["patient_id"]
prediction_time = spike["timestamp"]

baseline = calculate_historical_baseline(
    readings=readings,
    prediction_time=prediction_time,
    patient_id=patient_id,
)

future = find_future_glucose(
    readings=readings,
    prediction_time=prediction_time,
    patient_id=patient_id,
)

print("PATIENT:")
print(patient_id)

print()
print("PREDICTION TIME:")
print(prediction_time)

print()
print("CURRENT GLUCOSE:")
print(spike["glucose"])

print()
print("HISTORICAL BASELINE:")
print(baseline)

print()
print("FUTURE READING:")
print(future)

print()
print("FUTURE - BASELINE:")
print(
    future["glucose_level"] - baseline
)