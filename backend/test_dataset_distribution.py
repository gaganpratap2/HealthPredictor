import random
from collections import Counter
from datetime import datetime

from app.ml.synthetic_generator import generate_population
from app.ml.population_dataset import build_population_dataset
from app.ml.dataset_split import split_by_patient


rng = random.Random(42)

readings = generate_population(
    number_of_patients=10,
    start_time=datetime(2026, 1, 1),
    number_of_days=3,
    rng=rng,
)

dataset = build_population_dataset(readings)


train, validation, test = split_by_patient(
    dataset=dataset,
    train_patients=[1, 2, 3, 4, 5, 6],
    validation_patients=[7, 8],
    test_patients=[9, 10],
)


def print_distribution(name, data):
    labels = [
        observation["target_glucose_spike"]
        for observation in data
    ]

    counts = Counter(labels)

    total = len(labels)
    spikes = counts.get(1, 0)
    normal = counts.get(0, 0)

    print(name)
    print("Total:", total)
    print("Normal:", normal)
    print("Spikes:", spikes)

    if total > 0:
        print(
            "Spike rate:",
            round(spikes / total * 100, 2),
            "%",
        )

    print()


print_distribution("TRAIN", train)
print_distribution("VALIDATION", validation)
print_distribution("TEST", test)


print("PER PATIENT")
print()

patient_ids = sorted(
    set(
        observation["patient_id"]
        for observation in dataset
    )
)

for patient_id in patient_ids:
    patient_data = [
        observation
        for observation in dataset
        if observation["patient_id"] == patient_id
    ]

    spikes = sum(
        observation["target_glucose_spike"]
        for observation in patient_data
    )

    print(
        f"Patient {patient_id}: "
        f"{len(patient_data)} observations, "
        f"{spikes} spikes, "
        f"{round(spikes / len(patient_data) * 100, 2)}%"
    )