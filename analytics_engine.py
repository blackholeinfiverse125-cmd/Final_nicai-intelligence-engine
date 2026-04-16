def analyze_signal(signal):

    # -----------------------------
    # 🔹 INPUT SAFETY
    # -----------------------------
    if not isinstance(signal, dict):
        return {
            "risk_level": "LOW",
            "anomaly_score": 0.0,
            "anomaly_type": "INVALID_SIGNAL",
            "explanation": "Signal format invalid",
            "recommendation_signal": "MONITOR"
        }

    # -----------------------------
    # 🔹 SAFE EXTRACTION
    # -----------------------------
    value = signal.get("value", 0)

    try:
        value = float(value)
    except:
        value = 0

    feature = signal.get("feature_type") or ""
    feature = str(feature).lower()

    # -----------------------------
    # 🔹 DEFAULT STATE
    # -----------------------------
    risk_level = "LOW"
    anomaly_score = 0.2
    anomaly_type = "NORMAL"
    explanation = "Everything normal"

    # -----------------------------
    # 🌡 TEMPERATURE
    # -----------------------------
    if feature == "temperature":

        if value >= 45:
            risk_level = "HIGH"
            anomaly_score = 0.9
            anomaly_type = "TEMPERATURE_SPIKE"
            explanation = "Extreme temperature detected"

        elif value >= 38:
            risk_level = "MEDIUM"
            anomaly_score = 0.6
            anomaly_type = "TEMPERATURE_RISE"
            explanation = "Temperature rising above safe threshold"

    # -----------------------------
    # 🌫 AQI
    # -----------------------------
    elif feature == "aqi":

        if value >= 300:
            risk_level = "HIGH"
            anomaly_score = 0.95
            anomaly_type = "SEVERE_AIR_POLLUTION"
            explanation = "Air quality extremely hazardous"

        elif value >= 200:
            risk_level = "MEDIUM"
            anomaly_score = 0.7
            anomaly_type = "HIGH_POLLUTION"
            explanation = "Air quality unhealthy"

    # -----------------------------
    # 🚦 TRAFFIC
    # -----------------------------
    elif feature == "traffic":

        if value >= 90:
            risk_level = "HIGH"
            anomaly_score = 0.85
            anomaly_type = "TRAFFIC_CONGESTION"
            explanation = "Severe traffic congestion detected"

        elif value >= 70:
            risk_level = "MEDIUM"
            anomaly_score = 0.6
            anomaly_type = "HEAVY_TRAFFIC"
            explanation = "Traffic density increasing"

    # -----------------------------
    # 🎯 FINAL DECISION
    # -----------------------------
    if risk_level == "HIGH":
        recommendation = "ESCALATE"
    elif risk_level == "MEDIUM":
        recommendation = "INVESTIGATE"
    else:
        recommendation = "MONITOR"

    return {
        "risk_level": risk_level,
        "anomaly_score": anomaly_score,
        "anomaly_type": anomaly_type,
        "explanation": explanation,
        "recommendation_signal": recommendation
    }
