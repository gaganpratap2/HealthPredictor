def group_readings_by_patient(readings):
    grouped = {}

    for reading in readings:
        patient_id = reading["patient_id"]

        if patient_id not in grouped:
            grouped[patient_id] = []

        grouped[patient_id].append(reading)

    return grouped