def analyze_signal(validation_output):

    confidence = validation_output["confidence_score"]

    # simple deterministic anomaly logic
    anomaly_score = round(1 - confidence, 2)

    if anomaly_score > 0.7:
        priority = "HIGH"
    elif anomaly_score > 0.3:
        priority = "MEDIUM"
    else:
        priority = "LOW"

    return {
        "signal_id": validation_output["signal_id"],
        "status": validation_output["status"],
        "confidence_score": confidence,
        "anomaly_score": anomaly_score,
        "priority": priority
    }