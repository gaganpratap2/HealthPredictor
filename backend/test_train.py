from app.ml.preprocessing import (
    fit_scaler,
    transform_features,
)

from app.ml.train import train_logistic_regression


X_train = [
    [100, 70],
    [105, 72],
    [110, 75],
    [130, 90],
    [140, 95],
    [150, 100],
]

y_train = [
    0,
    0,
    0,
    1,
    1,
    1,
]


scaler = fit_scaler(X_train)

X_train_scaled = transform_features(
    scaler,
    X_train,
)


model = train_logistic_regression(
    X_train=X_train_scaled,
    y_train=y_train,
)


print("Model trained successfully")

predictions = model.predict(
    X_train_scaled
)

probabilities = model.predict_proba(
    X_train_scaled
)

print("Predictions:")
print(predictions)

print()

print("Probabilities:")
print(probabilities)