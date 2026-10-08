def analyze_predictions(
    dataset,
    predictions,
    probabilities,
):
    false_positives = []
    false_negatives = []

    for observation, prediction, probability in zip(
        dataset,
        predictions,
        probabilities,
    ):
        actual = observation["target_glucose_spike"]

        if prediction == 1 and actual == 0:
            false_positives.append({
                "patient_id": observation["patient_id"],
                "timestamp": observation["timestamp"],
                "glucose": observation["glucose"],
                "glucose_baseline": observation["glucose_baseline"],
                "glucose_delta": observation["glucose_delta"],
                "probability": probability,
            })

        elif prediction == 0 and actual == 1:
            false_negatives.append({
                "patient_id": observation["patient_id"],
                "timestamp": observation["timestamp"],
                "glucose": observation["glucose"],
                "glucose_baseline": observation["glucose_baseline"],
                "glucose_delta": observation["glucose_delta"],
                "probability": probability,
            })

    return false_positives, false_negatives