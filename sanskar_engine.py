import json
import hashlib
from datetime import datetime, timezone
from collections import defaultdict

from error_handler import error_response


# -----------------------------
# ZONE DETECTION (FIXED SAFE)
# -----------------------------
def detect_zone(lat, lon):
    try:
        lat = float(lat)
        lon = float(lon)

        if lat > 23:
            return "North"
        elif lat > 20:
            return "Central"
        else:
            return "South"

    except:
        return "Unknown"


# =========================================================
# 🔹 SINGLE SIGNAL ANALYSIS
# =========================================================
def analyze_signal(signal):

    try:
        if not isinstance(signal, dict):
            return error_response("Invalid signal input (must be dict)")

        if not signal:
            return error_response("Empty signal received")

        if "value" not in signal:
            return error_response("Missing 'value' field")

        value = signal.get("value")

        if not isinstance(value, (int, float)):
            return error_response("Invalid value type (must be numeric)")

        feature = str(signal.get("feature_type", "")).lower()

        risk_level = "LOW"
        anomaly_score = 0.2
        anomaly_type = "NORMAL"
        explanation = "Everything normal"

        # -----------------------------
        # TEMPERATURE
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
        # AQI
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
        # TRAFFIC
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

        else:
            anomaly_type = "UNKNOWN_FEATURE"
            explanation = "Feature type not recognized"
            anomaly_score = 0.1

        # -----------------------------
        # TANTRA COMPLIANT OUTPUT
        # -----------------------------
        if risk_level == "HIGH":
            recommendation = "eligible_for_escalation"
        elif risk_level == "MEDIUM":
            recommendation = "requires_review"
        else:
            recommendation = "monitor"

        output = {
            "risk_level": risk_level,
            "anomaly_score": anomaly_score,
            "anomaly_type": anomaly_type,
            "explanation": explanation,
            "recommendation_signal": recommendation
        }

        # -----------------------------
        # LOGGING
        # -----------------------------
        try:
            log_entry = {
                "trace_id": signal.get("trace_id"),
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "type": "ANALYSIS",
                "data": output
            }

            with open("logs/anomaly_logs.json", "a") as f:
                f.write(json.dumps(log_entry, default=str) + "\n")

        except:
            pass

        return output

    except Exception as e:
        return error_response(str(e))


# =========================================================
# 🔹 MULTI-SIGNAL ANALYSIS (🔥 FIXED SAFE VERSION)
# =========================================================
def analyze_patterns(outputs):

    try:
        if not isinstance(outputs, list):
            return error_response("Invalid input (outputs must be list)")

        if len(outputs) == 0:
            return {
                "pattern_id": "PATTERN_NONE",
                "anomaly_count": 0,
                "affected_zones": [],
                "pattern_summary": "No data available",
                "pattern_type": "NO_PATTERN",
                "severity_trend": "NONE",
                "linked_traces": []
            }

        anomaly_count = 0
        affected_zones = set()
        linked_traces = []
        zone_frequency = defaultdict(int)

        for o in outputs:

            # 🔥 CRITICAL FIX
            if not isinstance(o, dict):
                continue

            risk = o.get("risk_level")
            trace_id = o.get("trace_id")
            anomaly_score = o.get("anomaly_score", 0)

            if risk == "HIGH" or anomaly_score >= 0.6:

                anomaly_count += 1

                # 🔥 SAFE TRACE
                if isinstance(trace_id, str):
                    linked_traces.append(trace_id)

                zone = detect_zone(
                    o.get("latitude"),
                    o.get("longitude")
                )

                # 🔥 SAFE SET ADD (FIX FOR YOUR ERROR)
                if isinstance(zone, str):
                    affected_zones.add(zone)
                    zone_frequency[zone] += 1
                else:
                    affected_zones.add("Unknown")
                    zone_frequency["Unknown"] += 1

        dominant_zone = (
            max(zone_frequency, key=zone_frequency.get)
            if zone_frequency else "Unknown"
        )

        trace_string = "".join(sorted(linked_traces))
        base_string = f"{dominant_zone}_{anomaly_count}_{trace_string}"

        pattern_id = "PATTERN_" + hashlib.sha256(
            base_string.encode()
        ).hexdigest()[:6]

        # -----------------------------
        # PATTERN LOGIC
        # -----------------------------
        if anomaly_count >= 5:
            severity_trend = "INCREASING"
            pattern_type = "CLUSTER_ANOMALY"
            summary = f"Clustered anomalies detected in {dominant_zone}"

        elif anomaly_count >= 2:
            severity_trend = "STABLE"
            pattern_type = "REPEATED_ANOMALY"
            summary = f"Moderate anomalies in {dominant_zone}"

        elif anomaly_count == 1:
            severity_trend = "LOW"
            pattern_type = "ISOLATED_EVENT"
            summary = f"Single anomaly in {dominant_zone}"

        else:
            severity_trend = "NONE"
            pattern_type = "NO_PATTERN"
            summary = "No anomalies detected"

        pattern_output = {
            "pattern_id": pattern_id,
            "anomaly_count": anomaly_count,
            "affected_zones": list(affected_zones),
            "pattern_summary": summary,
            "pattern_type": pattern_type,
            "severity_trend": severity_trend,
            "linked_traces": linked_traces
        }

        # -----------------------------
        # LOGGING
        # -----------------------------
        try:
            log_entry = {
                "trace_id": pattern_id,
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "type": "PATTERN",
                "data": pattern_output
            }

            with open("logs/pattern_logs.json", "a") as f:
                f.write(json.dumps(log_entry, default=str) + "\n")

        except:
            pass

        return pattern_output

    except Exception as e:
        return error_response(str(e))
    


class SanskarEngine:

    def __init__(self):
        pass

    def process(self, signals):
        processed = self.preprocess(signals)

        anomaly = self.detect_anomaly(processed)
        temporal = self.analyze_temporal(processed)
        spatial = self.analyze_spatial(processed)
        risk = self.calculate_risk(processed, anomaly, temporal)
        confidence = self.calculate_confidence(processed)
        explanation = self.generate_explanation(processed, anomaly, temporal, spatial)

        return {
            "risk_level": risk,
            "anomaly_type": anomaly,
            "temporal_context": temporal,
            "spatial_context": spatial,
            "confidence": confidence,
            "explanation": explanation,
            "recommendation_signal": anomaly
        }

    def preprocess(self, signals):
        return {
            k: float(v) if isinstance(v, (int, float)) else v
            for k, v in signals.items()
        }
    def detect_anomaly(self, signals):

        pollution = signals.get("pollution", 0)
        temp = signals.get("temperature", 0)

        if pollution >= 300:
            return "severe_pollution"

        elif pollution >= 200:
            return "high_pollution"

    # ✅ check combined BEFORE moderate
        elif temp >= 35 and pollution >= 150:
            return "environmental_instability"

        elif pollution >= 150:
            return "moderate_pollution"

        return "normal"
    

    def analyze_temporal(self, signals):

        trend = signals.get("trend", 0)

        if trend > 0.7:
            return "RISING"
        elif trend < 0.3:
            return "FALLING"
        else:
            return "STABLE"

    def analyze_spatial(self, signals):

        zone = signals.get("zone", ["unknown"])

        if isinstance(zone, list) and len(zone) > 1:
            return "CLUSTERED"
        elif isinstance(zone, list):
            return zone[0]
        else:
            return "UNKNOWN"

    def calculate_risk(self, signals, anomaly, temporal):

        if anomaly in ["severe_pollution"]:
            return "HIGH"

        if anomaly in ["high_pollution", "environmental_instability"]:
            return "HIGH" if temporal == "RISING" else "MEDIUM"

        if anomaly in ["moderate_pollution"]:
            return "MEDIUM"

        return "LOW"

    def calculate_confidence(self, signals):

        pollution = signals.get("pollution", 0)
        temp = signals.get("temperature", 0)

        if pollution >= 200 or (pollution >= 150 and temp >= 35):
            return "HIGH"

        elif pollution >= 150:
            return "MEDIUM"

        else:
            return "LOW"

    def generate_explanation(self, signals, anomaly, temporal, spatial):

        pollution = signals.get("pollution", 0)
        temp = signals.get("temperature", 0)

        reasons = []

        if pollution >= 150:
            reasons.append("high pollution levels")

        if temp >= 35:
            reasons.append("elevated temperature")

        if reasons:
            reason_text = " and ".join(reasons)
        else:
            reason_text = "normal conditions"

        return f"{anomaly} detected in {spatial} with {temporal} trend due to {reason_text}."
