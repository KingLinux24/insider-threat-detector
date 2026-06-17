import pandas as pd
import joblib
from pathlib import Path

DATA = Path("data/processed/user_window_features.csv")
MODEL = Path("src/models/insider_iforest.joblib")
OUT = Path("data/processed/alerts.csv")

def main():
    df = pd.read_csv(DATA)
    model = joblib.load(MODEL)

    feature_cols = [
        "event_count",
        "unique_hosts",
        "off_hours_activity",
        "high_sensitivity_access_ratio",
        "data_transfer_sum",
        "privilege_change_flag",
    ]

    scores = -model.decision_function(df[feature_cols])
    df["anomaly_score"] = scores

    # Normalize to 0–1
    df["risk_score"] = (scores - scores.min()) / (scores.max() - scores.min())

    # Rule-based boosts
    df.loc[df["high_sensitivity_access_ratio"] > 0.5, "risk_score"] += 0.2
    df.loc[df["data_transfer_sum"] > 5_000_000, "risk_score"] += 0.2
    df.loc[df["off_hours_activity"] == True, "risk_score"] += 0.1

    df["risk_score"] = df["risk_score"].clip(0, 1)
    alerts = df[df["risk_score"] >= 0.7].sort_values("risk_score", ascending=False)

    OUT.parent.mkdir(parents=True, exist_ok=True)
    alerts.to_csv(OUT, index=False)

if __name__ == "__main__":
    main()
