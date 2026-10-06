from app.ml.target import calculate_glucose_spike


baseline = 110.0

print(
    "No spike:",
    calculate_glucose_spike(
        future_glucose=125.0,
        baseline_glucose=baseline,
    ),
)

print(
    "Spike:",
    calculate_glucose_spike(
        future_glucose=140.0,
        baseline_glucose=baseline,
    ),
)

print(
    "Large spike:",
    calculate_glucose_spike(
        future_glucose=150.0,
        baseline_glucose=baseline,
    ),
)

print(
    "Missing glucose:",
    calculate_glucose_spike(
        future_glucose=None,
        baseline_glucose=baseline,
    ),
)

print(
    "Missing baseline:",
    calculate_glucose_spike(
        future_glucose=140.0,
        baseline_glucose=None,
    ),
)