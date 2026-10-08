FEATURE_NAMES = [
    "glucose",
    "heart_rate",
    "hrv",
    "spo2",
    "steps",
    "glucose_baseline",
    "glucose_delta",
    "hour",
    "is_morning",
    "is_afternoon",
    "is_evening",
    "is_night",
    "meal_proximity_minutes",
    "minutes_until_next_meal",
    "glucose_rate",
]


def build_matrix(dataset):
    X = [
        [observation[name] for name in FEATURE_NAMES]
        for observation in dataset
    ]

    y = [
        observation["target_glucose_spike"]
        for observation in dataset
    ]

    return X, y