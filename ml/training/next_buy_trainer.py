import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import joblib
import os

MODEL_PATH = "backend/ml/models/next_buy_model.pkl"

def train_next_buy_model():
    """Simple placeholder model training for MVP."""

    # fake dataset for MVP
    df = pd.DataFrame({
        "purchases_last_30d": [0, 1, 5, 7, 10],
        "messages_sent": [2, 10, 25, 40, 55],
        "label": [0, 1, 1, 1, 1]
    })

    X = df[["purchases_last_30d", "messages_sent"]]
    y = df["label"]

    model = RandomForestClassifier(n_estimators=50)
    model.fit(X, y)

    os.makedirs(os.path.dirname(MODEL_PATH), exist_ok=True)
    joblib.dump(model, MODEL_PATH)

    return MODEL_PATH
