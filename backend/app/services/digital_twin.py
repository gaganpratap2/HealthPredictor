# What is the patient's current computational state?

from datetime import datetime
from app.services.anomaly_detection import (
    detect_glucose_anomaly,
    build_anomaly_context,
)
from app.services.time_features import detect_trend



def build_twin_state(
    patient_id,
    features,
    current_values,
    baseline_mean,
    baseline_std,
    data_quality,
):
    glucose_features = features.get("glucose_level", {})

    glucose = current_values.get("glucose_level")
    glucose_change = glucose_features.get("change")

    trend = detect_trend(glucose_change)

    if glucose is not None and baseline_mean is not None:
        deviation = glucose - baseline_mean
    else:
        deviation = None

    if deviation is not None and baseline_std:
        z_score = deviation / baseline_std
    else:
        z_score = None

    anomaly = detect_glucose_anomaly(
        z_score=z_score,
        trend=trend,
    )

    anomaly_context = build_anomaly_context(
    glucose_anomaly=anomaly,
    data_quality=data_quality,
    current_values=current_values,
    )

    return {
        "patient_id": patient_id,
        "updated_at": datetime.utcnow(),

        "vitals": {
            "glucose": glucose,
            "heart_rate": current_values.get("heart_rate"),
            "hrv": current_values.get("hrv"),
            "spo2": current_values.get("spo2"),
        },

        "activity": {
            "steps": current_values.get("steps"),
            "state": current_values.get("activity_state"),
        },

        "sleep": {
            "state": current_values.get("sleep_state"),
        },

        "glucose_state": {
            "baseline": baseline_mean,
            "baseline_std": baseline_std,
            "deviation": deviation,
            "z_score": z_score,
            "change": glucose_change,
            "trend": trend,
        },

        "anomaly": anomaly,

        "data_quality": data_quality,

        "features": features,
    }