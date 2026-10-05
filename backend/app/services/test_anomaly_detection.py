from app.services.anomaly_detection import detect_glucose_anomaly


tests = [0.5, 2.1, 3.2, -3.5]

for z_score in tests:
    result = detect_glucose_anomaly(
        z_score=z_score,
        trend="stable",
    )

    print(f"z_score={z_score}: {result}")