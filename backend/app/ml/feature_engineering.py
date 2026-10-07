def build_feature_vector(
    observation,
):
    glucose = observation["glucose"]

    baseline = observation["glucose_baseline"]

    glucose_delta = (
        glucose - baseline
    )

    return {
        "glucose": glucose,

        "heart_rate":
            observation["heart_rate"],

        "hrv":
            observation["hrv"],

        "spo2":
            observation["spo2"],

        "steps":
            observation["steps"],

        "glucose_baseline":
            baseline,

        "glucose_delta":
            glucose_delta,
    }