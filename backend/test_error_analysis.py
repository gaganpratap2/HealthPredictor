from app.ml.error_analysis import analyze_predictions


dataset = [
    {
        "patient_id": 1,
        "timestamp": "2026-01-01 06:00",
        "glucose": 110,
        "glucose_baseline": 115,
        "glucose_delta": -5,
        "target_glucose_spike": 0,
    },
    {
        "patient_id": 1,
        "timestamp": "2026-01-01 07:00",
        "glucose": 112,
        "glucose_baseline": 115,
        "glucose_delta": -3,
        "target_glucose_spike": 1,
    },
]

predictions = [1, 0]
probabilities = [0.80, 0.30]

false_positives, false_negatives = analyze_predictions(
    dataset,
    predictions,
    probabilities,
)

print("False positives:")
print(false_positives)

print()

print("False negatives:")
print(false_negatives)