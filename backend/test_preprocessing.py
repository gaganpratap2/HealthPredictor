from app.ml.preprocessing import (
    fit_scaler,
    transform_features,
)


X_train = [
    [100, 70],
    [110, 80],
    [120, 90],
]

X_test = [
    [105, 75],
]


scaler = fit_scaler(X_train)

X_train_scaled = transform_features(
    scaler,
    X_train,
)

X_test_scaled = transform_features(
    scaler,
    X_test,
)

print("Scaled training data:")
print(X_train_scaled)

print()

print("Scaled test data:")
print(X_test_scaled)