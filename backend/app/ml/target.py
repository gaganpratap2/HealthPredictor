SPIKE_THRESHOLD = 25.0


def calculate_glucose_spike(
    future_glucose,
    baseline_glucose,
):
    if future_glucose is None:
        return None

    if baseline_glucose is None:
        return None

    deviation = future_glucose - baseline_glucose

    return int(deviation >= SPIKE_THRESHOLD)

# Given future glucose and the patient's baseline, determine whether the future observation represents a spike.