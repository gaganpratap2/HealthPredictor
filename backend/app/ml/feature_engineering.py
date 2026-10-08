from datetime import datetime


def calculate_glucose_rate(
    current_glucose,
    previous_glucose,
    minutes,
):
    if (
        current_glucose is None
        or previous_glucose is None
        or minutes <= 0
    ):
        return None

    return (
        current_glucose - previous_glucose
    ) / minutes


def calculate_time_features(timestamp):
    hour = timestamp.hour

    return {
        "hour": hour,
        "is_morning": int(6 <= hour < 12),
        "is_afternoon": int(12 <= hour < 18),
        "is_evening": int(18 <= hour < 23),
        "is_night": int(hour >= 23 or hour < 6),
    }


def calculate_meal_proximity(
    timestamp,
    meal_hours=(8, 13, 19),
):
    current_minutes = (
        timestamp.hour * 60
        + timestamp.minute
    )

    distances = []

    for meal_hour in meal_hours:
        meal_minutes = meal_hour * 60

        distance = abs(
            current_minutes - meal_minutes
        )

        distances.append(distance)

    return min(distances)


def build_feature_vector(
    observation,
    previous_observation=None,
):
    glucose = observation["glucose"]
    baseline = observation["glucose_baseline"]

    glucose_delta = (
        glucose - baseline
    )

    features = {
        "glucose": glucose,
        "heart_rate": observation["heart_rate"],
        "hrv": observation["hrv"],
        "spo2": observation["spo2"],
        "steps": observation["steps"],
        "glucose_baseline": baseline,
        "glucose_delta": glucose_delta,
    }

    timestamp = observation["timestamp"]

    features["minutes_until_next_meal"] = (
        calculate_minutes_until_next_meal(timestamp)
    )

    time_features = calculate_time_features(
        timestamp
    )

    features.update(time_features)

    features["meal_proximity_minutes"] = (
        calculate_meal_proximity(timestamp)
    )

    if previous_observation is not None:
        previous_glucose = (
            previous_observation["glucose"]
        )

        time_difference = (
            timestamp
            - previous_observation["timestamp"]
        ).total_seconds() / 60

        features["glucose_rate"] = (
            calculate_glucose_rate(
                current_glucose=glucose,
                previous_glucose=previous_glucose,
                minutes=time_difference,
            )
        )
    else:
        features["glucose_rate"] = None

    return features

def calculate_minutes_until_next_meal(
    timestamp,
    meal_hours=(8, 13, 19),
):
    current_minutes = (
        timestamp.hour * 60
        + timestamp.minute
    )

    meal_minutes = [
        hour * 60
        for hour in meal_hours
    ]

    future_meals = [
        meal
        for meal in meal_minutes
        if meal > current_minutes
    ]

    if future_meals:
        return min(future_meals) - current_minutes

    # Next day's breakfast
    first_meal = meal_minutes[0]

    return (
        24 * 60
        - current_minutes
        + first_meal
    )