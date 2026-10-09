
from sklearn.metrics import (
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix,
)


def analyze_thresholds(y_true, probabilities):
    thresholds = [0.30, 0.40, 0.50, 0.60, 0.70, 0.80, 0.90]

    print("\n====== VALIDATION THRESHOLD ANALYSIS ======")

    for threshold in thresholds:
        predictions = [
            int(probability >= threshold)
            for probability in probabilities
        ]

        precision = precision_score(
            y_true,
            predictions,
            zero_division=0,
        )

        recall = recall_score(
            y_true,
            predictions,
            zero_division=0,
        )

        f1 = f1_score(
            y_true,
            predictions,
            zero_division=0,
        )

        matrix = confusion_matrix(
            y_true,
            predictions,
            labels=[0, 1],
        )

        tn, fp, fn, tp = matrix.ravel()

        print(
            f"Threshold={threshold:.2f} | "
            f"Precision={precision:.3f} | "
            f"Recall={recall:.3f} | "
            f"F1={f1:.3f} | "
            f"FP={fp} | FN={fn} | "
            f"TP={tp} | TN={tn}"
        )
