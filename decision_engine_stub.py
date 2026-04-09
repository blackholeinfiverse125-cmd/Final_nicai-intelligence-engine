def make_decision(analytics_output):

    anomaly = analytics_output["anomaly_score"]

    if anomaly > 0.6:
        decision = "ALERT"
        risk = "HIGH"
    elif anomaly > 0.3:
        decision = "REVIEW"
        risk = "MEDIUM"
    else:
        decision = "PROCEED"
        risk = "LOW"

    return {
        "decision": decision,
        "risk_level": risk,
        "reason": "Decision based on anomaly score"
    }