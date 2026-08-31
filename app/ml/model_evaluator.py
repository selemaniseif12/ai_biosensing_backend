# app/ml/model_evaluator.py

import numpy as np
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from app.ml.model_loader import load_v2_model, load_v6_model

def evaluate_model(model, X_test, y_test, model_name="model"):
    """
    Evaluates a trained model using accuracy, classification report,
    and confusion matrix.

    Parameters:
        model: Trained ML model
        X_test (np.ndarray): Test feature matrix
        y_test (np.ndarray): Test labels
        model_name (str): Name of the model for printing

    Returns:
        dict: Evaluation results
    """

    print(f"\nEvaluating {model_name}...")

    y_pred = model.predict(X_test)

    acc = accuracy_score(y_test, y_pred)
    report = classification_report(y_test, y_pred)
    matrix = confusion_matrix(y_test, y_pred)

    print(f"Accuracy ({model_name}): {acc:.4f}")
    print(f"\nClassification Report ({model_name}):\n{report}")
    print(f"\nConfusion Matrix ({model_name}):\n{matrix}")

    return {
        "accuracy": acc,
        "classification_report": report,
        "confusion_matrix": matrix
    }


def evaluate_v2(X_test, y_test):
    """
    Loads and evaluates the 100-virus V2 model.
    """
    model = load_v2_model()
    return evaluate_model(model, X_test, y_test, model_name="V2")


def evaluate_v6(X_test, y_test):
    """
    Loads and evaluates the 100-virus V6 model.
    """
    model = load_v6_model()
    return evaluate_model(model, X_test, y_test, model_name="V6")
