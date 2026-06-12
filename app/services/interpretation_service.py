def interpret_result(prediction: int, confidence: float) -> str:
    """
    Convert ML prediction + confidence into a human-readable biosensing interpretation.
    """

    # High confidence threshold
    HIGH = 0.80
    MEDIUM = 0.55

    if prediction == 1:
        if confidence >= HIGH:
            return "Pathogen detected with high confidence. Immediate follow-up recommended."
        elif confidence >= MEDIUM:
            return "Pathogen likely detected. Additional verification is advised."
        else:
            return "Possible pathogen presence, but confidence is low. Retesting recommended."

    else:  # prediction == 0
        if confidence >= HIGH:
            return "No pathogen detected with high confidence."
        elif confidence >= MEDIUM:
            return "No pathogen detected, but confidence is moderate. Consider retesting if symptoms persist."
        else:
            return "Uncertain result. Confidence is low. Retesting recommended."
