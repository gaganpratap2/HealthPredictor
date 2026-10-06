from statistics import mean


def calculate_historical_baseline(
    readings,
    prediction_time,
):
    historical_values = [
        reading["glucose_level"]
        for reading in readings
        if (
            reading["timestamp"] < prediction_time
            and reading.get("glucose_level") is not None
        )
    ]

    if not historical_values:
        return None

    return mean(historical_values)