from sklearn.metrics import (
    precision_score,
    recall_score,
    f1_score,
    average_precision_score,
    confusion_matrix,
)


def evaluate_classifier(
    y_true,
    predictions,
    probabilities,
):
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

    pr_auc = average_precision_score(
        y_true,
        probabilities,
    )

    matrix = confusion_matrix(
        y_true,
        predictions,
    )

    return {
        "precision": precision,
        "recall": recall,
        "f1": f1,
        "pr_auc": pr_auc,
        "confusion_matrix": matrix,
    }