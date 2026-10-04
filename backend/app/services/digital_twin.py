from datetime import datetime

from app.services.time_features import (
    calculate_z_score,
    detect_trend,
)


def build_twin_state(
    patient_id,
    features,
    current_values,
    baseline_mean,
    baseline_std,
    data_quality,
):
    glucose_features = features.get(
        "glucose_level",
        {}
    )

    glucose = current_values.get(
        "glucose_level"
    )

    glucose_change = glucose_features.get(
        "change"
    )

    glucose_z_score = calculate_z_score(
        current_value=glucose,
        baseline_mean=baseline_mean,
        baseline_std=baseline_std,
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
            "deviation": (
                glucose - baseline_mean
                if glucose is not None
                and baseline_mean is not None
                else None
            ),
            "z_score": glucose_z_score,
            "change": glucose_change,
            "trend": detect_trend(glucose_change),
        },

        "data_quality": data_quality,

        "features": features,
    }