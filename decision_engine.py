def make_decision(analytics):

    anomaly = analytics["anomaly_score"]

    if anomaly > 0.7:
        decision = "ALERT"
        risk = "HIGH"
    elif anomaly > 0.4:
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