from app.ml.future_target import find_future_glucose
from app.ml.historical_baseline import calculate_historical_baseline
from app.ml.target import calculate_glucose_spike


def build_prediction_observation(
    reading,
    all_readings,
):
    prediction_time = reading["timestamp"]

    baseline_glucose = calculate_historical_baseline(
        readings=all_readings,
        prediction_time=prediction_time,
    )

    if baseline_glucose is None:
        return None

    future = find_future_glucose(
        readings=all_readings,
        prediction_time=prediction_time,
    )

    if future is None:
        return None

    future_glucose = future["glucose_level"]

    spike = calculate_glucose_spike(
        future_glucose=future_glucose,
        baseline_glucose=baseline_glucose,
    )

    if spike is None:
        return None

    return {
        "patient_id": reading["patient_id"],
        "timestamp": prediction_time,

        "glucose": reading.get("glucose_level"),
        "heart_rate": reading.get("heart_rate"),
        "hrv": reading.get("hrv"),
        "spo2": reading.get("spo2"),
        "steps": reading.get("steps"),

        "glucose_baseline": baseline_glucose,

        "target_future_glucose": future_glucose,
        "target_glucose_spike": spike,
    }