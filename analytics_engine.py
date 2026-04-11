def analyze_signal(signal):

    value = signal.get("value", 0)

    # deterministic anomaly scoring
    if value >= 90:
        anomaly_score = 0.9
        priority = "HIGH"

    elif value >= 70:
        anomaly_score = 0.55
        priority = "MEDIUM"

    else:
        anomaly_score = 0.08
        priority = "LOW"

    return {
        "signal_id": signal["signal_id"],
        "status": signal["status"],
        "confidence_score": signal["confidence_score"],
        "anomaly_score": anomaly_score,
        "priority": priority
    }