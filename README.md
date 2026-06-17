
# Insider Threat Detector: Behavioral Risk Scoring Engine

An early-warning, privacy-aware security prototype designed to identify risky internal behaviors by combining statistical anomaly detection (**Isolation Forest**) with risk-prioritizing business rules. 

Rather than definitively accusing or labeling users as malicious, this system surfaces behavioral anomalies over rolling windows, producing transparent risk scores accompanied by explainable indicators for human analyst review.

---

## 📌 Principles & Ethical Framework

Detecting insider threats requires balancing organizational security with workforce trust. This project is built on the following core principles:

* **Behavior Over Content:** The system analyzes metadata (when, where, and how much) rather than inspecting document contents, keystrokes, or private communications. 
* **Risk Scoring vs. Accusation:** A high risk score is *not* an accusation of guilt. It indicates a statistical departure from an established baseline that warrants contextual evaluation.
* **Human-in-the-Loop (HITL):** This engine serves strictly as a prioritization tool for security analysts, preventing automated disciplinary actions or immediate access terminations based solely on algorithmic output.

---

## 📊 Behavioral Signals (Privacy-Aware)

To preserve privacy while maintaining a robust security posture, the system monitors telemetry points devoid of Deep Packet Inspection (DPI) or invasive host monitoring:

| Signal Type | Monitored Attribute | Intent/Detection Value |
| :--- | :--- | :--- |
| **Velocity Spikes** | `event_count` over a 1-hour window | Detects rapid automated data harvesting or credential compromise. |
| **Temporal Shifts** | `off_hours_activity` | Pinpoints unusual access outside of a user's standard working hours. |
| **Scope Expansion** | `unique_hosts` count | Catches potential lateral movement across different corporate network assets. |
| **Sensitivity Focus** | `high_sensitivity_access_ratio` | Flags concentrated interaction with high-value assets outside role norms. |
| **Data Exfiltration Proxy** | `data_transfer_sum` | Identifies bulk file movement or staging of corporate intellectual property. |

---

## ⚙️ How it Maps to Real-World UEBA Tools

Commercial **User and Entity Behavior Analytics (UEBA)** tools (e.g., Exabeam, Securonix, Splunk UBA) use a highly similar architecture to this repository:

1. **Ingestion:** Real platforms ingest logs from SIEMs (Splunk, Elastic) or Identity Providers (Okta, Active Directory) using a schema similar to our `events.jsonl`.
2. **Baselines:** They establish peer-group baselines (e.g., comparing Alice's actions against others in the `finance` department).
3. **Hybrid Scoring:** Like our Isolation Forest + Rule Boost combination, enterprise engines use machine learning to catch unknown anomalies and explicit deterministic rules to flag known policy violations.

---

## 🛡️ Privacy Safeguards & Limitations

* **No PII or Content Processing:** We process no cleartext messages, emails, files, or specific URLs.
* **Data Aggregation:** Raw event sequences are condensed into hourly window statistics, eliminating micro-tracking of every mouse click.
* **Limitation (Cold Start):** The Isolation Forest requires a clean historical baseline. If an insider is already acting maliciously during the training phase, their behavior will be baselined as "normal."
* **Limitation (Context Blindness):** The model cannot know if a spike in data transfer is due to a legitimate, urgent end-of-quarter financial audit.

---

## 🔍 Example Alert with Explanation

When a window exceeds the critical risk threshold (>= 0.7), the scoring engine yields a structured telemetry log for the analyst interface:

### JSON Payload
```json
{
  "user_id": "alice",
  "window": "2026-06-17T16:00:00Z",
  "risk_score": 0.92,
  "anomaly_score": 0.384,
  "explanations": [
    "Unusually large data transfer volume",
    "High proportion of access to sensitive resources",
    "Activity outside normal business hours"
  ]
}

```

### Triaging False Positives
An analyst reviewing this alert would check for standard business exemptions before escalating:

* Did Alice's manager authorize an off-hours database migration?

* Is there a scheduled batch backup job configured under Alice's service account role?

## 🚀 Quickstart & Pipeline Execution
1. Environment Setup:

```Bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```
2. Execute Engine Pipeline:

```Bash
# 1. Generate synthetic logs
python src/data/generate_events.py

# 2. Extract window features
python src/features/build_features.py

# 3. Train the Isolation Forest baseline
python src/models/train.py

# 4. Compute risk scores and compile alerts
python src/scoring/score.py

```
3. Launch the Analyst API:

```Bash
uvicorn src.api.app:app --reload --port 8000
```
Access the active alert endpoints at http://127.0.0.1:8000/alerts

