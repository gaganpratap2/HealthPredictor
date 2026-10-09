
def analyze_logistic_coefficients(model, feature_names):
    coefficients = model.coef_[0]

    ranked_features = sorted(
        zip(feature_names, coefficients),
        key=lambda item: abs(item[1]),
        reverse=True,
    )

    print("\n====== LOGISTIC REGRESSION FEATURE ANALYSIS ======")
    print("Feature                         Coefficient")

    for name, coefficient in ranked_features:
        print(f"{name:30} {coefficient: .4f}")

    print("\nInterpretation:")
    print("Positive coefficient: associated with higher predicted spike odds.")
    print("Negative coefficient: associated with lower predicted spike odds.")
    print("Magnitude reflects influence on the model's log-odds.")
