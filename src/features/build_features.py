import json
import pandas as pd
from pathlib import Path

IN = Path("data/raw/events.jsonl")
OUT = Path("data/processed/user_window_features.csv")
OUT.parent.mkdir(parents=True, exist_ok=True)

def main():
    rows = []
    with IN.open("r") as f:
        for line in f:
            rows.append(json.loads(line))

    df = pd.DataFrame(rows)
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df["window"] = df["timestamp"].dt.floor("1h")

    df["off_hours"] = ~df["timestamp"].dt.hour.between(8, 18)
    df["is_high_sensitive"] = (df["resource_sensitivity"] == "high").astype(int)
    df["is_priv_change"] = (df["event_type"] == "privilege_change").astype(int)

    grouped = df.groupby(["user_id", "window"]).agg(
        event_count=("event_type", "count"),
        unique_hosts=("host", "nunique"),
        off_hours_activity=("off_hours", "max"),
        high_sensitivity_access_ratio=("is_high_sensitive", "mean"),
        data_transfer_sum=("bytes_transferred", "sum"),
        privilege_change_flag=("is_priv_change", "max"),
        insider_label=("label", "max")
    ).reset_index()

    grouped.to_csv(OUT, index=False)

if __name__ == "__main__":
    main()
