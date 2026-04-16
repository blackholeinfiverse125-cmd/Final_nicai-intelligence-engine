def analyze_signal(signal):

    value = signal.get("value", 0)
    feature = signal.get("feature_type", "").lower()

    risk_level = "LOW"
    anomaly_score = 0.2
    anomaly_type = "NORMAL"
    explanation = "Everything normal"

    # 🌡 Temperature Analysis
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

    # 🌫 AQI Analysis
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

    # 🚦 Traffic Analysis
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

    # 🎯 Recommendation logic
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