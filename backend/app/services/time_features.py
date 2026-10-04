from datetime import datetime, timedelta
from statistics import mean, stdev

def calculate_basic_features(readings):
    if not readings:
        return {}

    readings = sorted(
        readings,
        key=lambda reading: reading["timestamp"]
    )

    values = [
        reading["value"]
        for reading in readings
    ]

    return {
        "mean": sum(values) / len(values),
        "minimum": min(values),
        "maximum": max(values),
        "change": values[-1] - values[0],
    }

def get_recent_readings(readings, current_time, minutes):
    start_time = current_time - timedelta(minutes=minutes)

    return [
        reading
        for reading in readings
        if start_time <= reading["timestamp"] <= current_time
    ]

def calculate_window_features(readings, current_time, minutes):
    recent_readings = get_recent_readings(
        readings,
        current_time,
        minutes
    )

    return calculate_basic_features(recent_readings)


def calculate_signal_features(readings, signal):
    readings = sorted(
        readings,
        key=lambda reading: reading["timestamp"]
    )

    values = [
        reading[signal]        # reading[signal] means:Get the value from the reading dictionary using signal as the key.
        for reading in readings
        if reading.get(signal) is not None
    ]

    if not values:
        return {}

    return {
        "mean": sum(values) / len(values),
        "minimum": min(values),
        "maximum": max(values),
        "change": values[-1] - values[0],
        "count": len(values),
    }


def calculate_multi_signal_features(readings):
    signals = [
        "glucose_level",
        "heart_rate",
        "hrv",
        "spo2",
        "steps",
    ]

    features = {}

    for signal in signals:
        features[signal] = calculate_signal_features(
            readings,
            signal
        )

    return features


def calculate_baseline(values):
    if not values:
        return None

    return sum(values) / len(values)

def calculate_deviation(current_value, baseline):
    if current_value is None or baseline is None:
        return None

    return current_value - baseline


def calculate_baseline_stats(values):
    if not values:
        return {}

    result = {
        "mean": mean(values),
        "count": len(values),
    }

    if len(values) >= 2:
        result["std"] = stdev(values)
    else:
        result["std"] = None

    return result


def build_personalized_state(
    historical_values,
    current_value
):
    baseline = calculate_baseline_stats(
        historical_values
    )

    deviation = calculate_deviation(
        current_value,
        baseline.get("mean")
    )

    return {
        "current_value": current_value,
        "baseline_mean": baseline.get("mean"),
        "baseline_std": baseline.get("std"),
        "baseline_count": baseline.get("count"),
        "deviation": deviation,
    }


def detect_trend(change, threshold=2.0):
    if change is None:
        return "unknown"

    if change > threshold:
        return "rising"

    if change < -threshold:
        return "falling"

    return "stable"

features = {
    "mean": 120,
    "minimum": 100,
    "maximum": 135,
    "change": 35,
}

features["trend"] = detect_trend(
    features["change"]
)



def calculate_current_values(readings):
    if not readings:
        return {}

    readings = sorted(
        readings,
        key=lambda reading: reading["timestamp"]
    )

    latest = readings[-1]

    signals = [
        "glucose_level",
        "heart_rate",
        "hrv",
        "spo2",
        "steps",
        "activity_state",
        "sleep_state",
    ]

    return {
        signal: latest.get(signal)
        for signal in signals
    }



from statistics import mean, stdev


def calculate_baseline_stats(values):
    if not values:
        return {}

    result = {
        "mean": mean(values),
        "count": len(values),
    }

    if len(values) >= 2:
        result["std"] = stdev(values)
    else:
        result["std"] = None

    return result


def calculate_z_score(
    current_value,
    baseline_mean,
    baseline_std,
):
    if current_value is None:
        return None

    if baseline_mean is None:
        return None

    if baseline_std is None or baseline_std == 0:
        return None

    return (
        (current_value - baseline_mean)
        / baseline_std
    )