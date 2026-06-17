import pandas as pd
import joblib
from pathlib import Path
from sklearn.ensemble import IsolationForest

DATA = Path("data/processed/user_window_features.csv")
MODEL_OUT = Path("src/models/insider_iforest.joblib")

def main():
    df = pd.read_csv(DATA)

    feature_cols = [
        "event_count",
        "unique_hosts",
        "off_hours_activity",
        "high_sensitivity_access_ratio",
        "data_transfer_sum",
        "privilege_change_flag",
    ]

    X = df[feature_cols]

    model = IsolationForest(
        n_estimators=400,
        contamination=0.05,
        random_state=42
    )

    model.fit(X)
    MODEL_OUT.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(model, MODEL_OUT)

if __name__ == "__main__":
    main()
