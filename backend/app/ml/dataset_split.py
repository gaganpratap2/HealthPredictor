def split_by_patient(
    dataset,
    train_patients,
    validation_patients,
    test_patients,
):
    train = []
    validation = []
    test = []

    for observation in dataset:
        patient_id = observation["patient_id"]

        if patient_id in train_patients:
            train.append(observation)

        elif patient_id in validation_patients:
            validation.append(observation)

        elif patient_id in test_patients:
            test.append(observation)

    return train, validation, test