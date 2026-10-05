# Is something unusual?

def detect_glucose_anomaly(z_score, trend):
    if z_score is None:
        return {
            "is_anomaly": False,
            "severity": "unknown",
            "direction": "unknown",
            "reason": "Insufficient baseline data",
        }

    if abs(z_score) < 2:
        severity = "normal"
        is_anomaly = False
        direction = "within_expected_range"

    elif z_score > 0:
        severity = "high" if abs(z_score) >= 3 else "medium"
        is_anomaly = True
        direction = "above_baseline"

    else:
        severity = "high" if abs(z_score) >= 3 else "medium"
        is_anomaly = True
        direction = "below_baseline"

    if not is_anomaly:
        reason = "Glucose is within the expected personal range"
    elif direction == "above_baseline":
        reason = "Glucose is unusually above the patient's baseline"
    else:
        reason = "Glucose is unusually below the patient's baseline"

    return {
        "is_anomaly": is_anomaly,
        "severity": severity,
        "direction": direction,
        "reason": reason,
    }


def build_anomaly_context(
    glucose_anomaly,
    data_quality,
    current_values,
):
    context = {
        "glucose": glucose_anomaly,
        "data_quality": data_quality,
        "signals": {
            "heart_rate": current_values.get("heart_rate"),
            "hrv": current_values.get("hrv"),
            "spo2": current_values.get("spo2"),
            "activity_state": current_values.get("activity_state"),
        },
    }

    return context