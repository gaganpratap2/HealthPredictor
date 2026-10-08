from app.ml.dataset_builder import build_patient_dataset
from app.ml.patient_data import group_readings_by_patient


def build_population_dataset(readings):
    grouped = group_readings_by_patient(readings)

    dataset = []

    for patient_id, patient_readings in grouped.items():
        patient_dataset = build_patient_dataset(
            patient_readings
        )

        dataset.extend(patient_dataset)

    return dataset