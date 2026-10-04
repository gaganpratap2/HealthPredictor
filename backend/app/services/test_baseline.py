from app.services.time_features import (
    calculate_baseline_stats,
    calculate_z_score,
)


values = [118.5, 115.2, 125]

baseline = calculate_baseline_stats(values)

print("BASELINE")
print(baseline)

z_score = calculate_z_score(
    current_value=135,
    baseline_mean=baseline["mean"],
    baseline_std=baseline["std"],
)

print("\nZ-SCORE")
print(z_score)