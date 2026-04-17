from collections import defaultdict
import hashlib
import json


# -----------------------------
# ZONE DETECTION (single source)
# -----------------------------
def detect_zone(lat, lon):
    if lat is None or lon is None:
        return "Unknown"

    if lat > 23:
        return "North"
    elif lat > 20:
        return "Central"
    else:
        return "South"


# -----------------------------
# MULTI-SIGNAL ANALYSIS
# -----------------------------
def analyze_patterns(outputs):

    anomaly_count = 0
    affected_zones = set()
    linked_traces = []

    zone_frequency = defaultdict(int)

    # -----------------------------
    # LOOP THROUGH SIGNALS
    # -----------------------------
    for o in outputs:

        risk = o.get("risk_level")
        trace_id = o.get("trace_id")
        anomaly_score = o.get("anomaly_score", 0)

        if risk == "HIGH" or anomaly_score >= 0.6:

            anomaly_count += 1

            if trace_id:
                linked_traces.append(trace_id)

            # -----------------------------
            # ZONE DETECTION
            # -----------------------------
            lat = o.get("latitude")
            lon = o.get("longitude")

            zone = detect_zone(lat, lon)

            affected_zones.add(zone)
            zone_frequency[zone] += 1

    # -----------------------------
    # MOST AFFECTED ZONE
    # -----------------------------
    if zone_frequency:
        dominant_zone = max(zone_frequency, key=zone_frequency.get)
    else:
        dominant_zone = "Unknown"

    # -----------------------------
    # STRONG DETERMINISTIC PATTERN ID
    # -----------------------------
    trace_string = "".join(sorted(linked_traces))
    pattern_string = dominant_zone + "_" + str(anomaly_count) + "_" + trace_string

    pattern_id = "PATTERN_" + hashlib.sha256(pattern_string.encode()).hexdigest()[:6]

    # -----------------------------
    # SEVERITY TREND
    # -----------------------------
    if anomaly_count >= 5:
        severity_trend = "INCREASING"
    elif anomaly_count >= 2:
        severity_trend = "STABLE"
    else:
        severity_trend = "LOW"

    # -----------------------------
    # PATTERN TYPE
    # -----------------------------
    if anomaly_count >= 5:
        pattern_type = "CLUSTER_ANOMALY"
    elif anomaly_count >= 2:
        pattern_type = "REPEATED_ANOMALY"
    else:
        pattern_type = "ISOLATED_EVENT"

    # -----------------------------
    # SUMMARY
    # -----------------------------
    if anomaly_count >= 5:
        summary = f"Clustered anomalies detected in {dominant_zone}"
    elif anomaly_count > 0:
        summary = f"Moderate anomalies in {dominant_zone}"
    else:
        summary = "No major anomalies"

    # -----------------------------
    # FINAL OUTPUT
    # -----------------------------
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
    # OBSERVABILITY (MANDATORY)
    # -----------------------------
    try:
        with open("pattern_logs.json", "a") as f:
            f.write(json.dumps(pattern_output) + "\n")
    except:
        pass

    return pattern_output