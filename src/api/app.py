from fastapi import FastAPI
import pandas as pd

app = FastAPI(title="Insider Threat Detector", version="1.0")

@app.get("/alerts")
def alerts():
    df = pd.read_csv("data/processed/alerts.csv")
    return df.to_dict(orient="records")
