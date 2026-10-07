FEATURE_NAMES = [
    "glucose",
    "heart_rate",
    "hrv",
    "spo2",
    "steps",
    "glucose_baseline",
    "glucose_delta",
]


def build_matrix(dataset):
    X = [
        [
            observation[name]
            for name in FEATURE_NAMES
        ]
        for observation in dataset
    ]

    y = [
        observation["target_glucose_spike"]
        for observation in dataset
    ]

    return X, y