def check_wearable_event(event):
    issues = []

    if event.heart_rate is None:
        issues.append("missing_heart_rate")

    if event.hrv is None:
        issues.append("missing_hrv")

    if event.spo2 is None:
        issues.append("missing_spo2")

    if event.glucose_level is None:
        issues.append("missing_glucose")

    if event.spo2 is not None and not 0 <= event.spo2 <= 100:
        issues.append("invalid_spo2")

    if event.heart_rate is not None and event.heart_rate < 0:
        issues.append("invalid_heart_rate")

    if event.glucose_level is not None and event.glucose_level < 0:
        issues.append("invalid_glucose")

    return issues