import json
import random
from datetime import datetime, timedelta
from pathlib import Path

OUT = Path("data/raw/events.jsonl")
OUT.parent.mkdir(parents=True, exist_ok=True)

USERS = [
    {"id": "alice", "dept": "finance"},
    {"id": "bob", "dept": "engineering"},
    {"id": "carol", "dept": "hr"},
]

HOSTS = ["wkst-01", "wkst-02", "srv-fin-01", "srv-eng-01"]
IPS = ["10.0.1.10", "10.0.1.11", "10.0.2.20"]

def ts(base, minutes):
    return (base + timedelta(minutes=minutes)).isoformat() + "Z"

def main():
    base = datetime.utcnow() - timedelta(days=1)
    rows = []

    # Normal behavior
    for i in range(1200):
        u = random.choice(USERS)
        rows.append({
            "timestamp": ts(base, i),
            "user_id": u["id"],
            "department": u["dept"],
            "event_type": random.choice(["login", "file_access"]),
            "host": random.choice(HOSTS),
            "src_ip": random.choice(IPS),
            "success": True,
            "bytes_transferred": random.randint(100, 50_000),
            "resource_sensitivity": random.choice(["low", "medium"]),
            "label": 0
        })

    # Insider-like behavior (policy-violating, not proven malicious)
    for i in range(120):
        rows.append({
            "timestamp": ts(base, 1500 + i),
            "user_id": "alice",
            "department": "finance",
            "event_type": random.choice(["file_access", "data_transfer"]),
            "host": "srv-fin-01",
            "src_ip": "10.0.9.99",
            "success": True,
            "bytes_transferred": random.randint(1_000_000, 20_000_000),
            "resource_sensitivity": "high",
            "label": 1
        })

    random.shuffle(rows)

    with OUT.open("w", encoding="utf-8") as f:
        for r in rows:
            f.write(json.dumps(r) + "\n")

if __name__ == "__main__":
    main()
