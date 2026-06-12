from app.ml.model_loader import load_rf, load_xgboost

def classify(features):
    rf = load_rf()
    xgb = load_xgboost()

    rf_pred = rf.predict([features])[0]
    xgb_pred = xgb.predict([features])[0]

    avg = (rf_pred + xgb_pred) / 2.0

    return "Positive" if avg > 0.5 else "Negative"
