def explain(row):
    reasons = []

    if row["data_transfer_sum"] > 5_000_000:
        reasons.append("Unusually large data transfer volume")
    if row["high_sensitivity_access_ratio"] > 0.5:
        reasons.append("High proportion of access to sensitive resources")
    if row["off_hours_activity"]:
        reasons.append("Activity outside normal business hours")
    if row["unique_hosts"] > 3:
        reasons.append("Access across multiple hosts in short time")

    if not reasons:
        reasons.append("Behavior deviates from established baseline")

    return reasons
