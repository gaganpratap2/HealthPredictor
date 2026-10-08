from datetime import datetime

from app.ml.feature_engineering import (
    calculate_glucose_rate,
    calculate_time_features,
    calculate_meal_proximity,
)

from app.ml.feature_engineering import (
    calculate_minutes_until_next_meal,
)


print("Glucose rate:")

rate = calculate_glucose_rate(
    current_glucose=120,
    previous_glucose=110,
    minutes=5,
)

print(rate)

print()

print("Time features:")

features = calculate_time_features(
    datetime(2026, 1, 1, 8, 10)
)

print(features)

print()

print("Meal proximity:")

proximity = calculate_meal_proximity(
    datetime(2026, 1, 1, 8, 10)
)

print(proximity)

print()
print("Minutes until next meal:")

print(
    calculate_minutes_until_next_meal(
        datetime(2026, 1, 1, 6, 0)
    )
)

print(
    calculate_minutes_until_next_meal(
        datetime(2026, 1, 1, 7, 30)
    )
)

print(
    calculate_minutes_until_next_meal(
        datetime(2026, 1, 1, 9, 0)
    )
)