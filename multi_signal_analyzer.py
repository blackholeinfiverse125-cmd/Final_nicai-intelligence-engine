import hashlib
from collections import defaultdict


# -----------------------------
# 🔹 PATTERN ID GENERATOR
# -----------------------------
def generate_pattern_id(linked_traces):
    base = "".join(sorted(linked_traces))
    return "PATTERN_" + hashlib.sha256(base.encode()).hexdigest()[:6]


# -----------------------------
# 🔥 CORE ANALYSIS ENGINE
# -----------------------------
def analyze_patterns(outputs):

    anomaly_count = 0
    affected_zones = set()
    linked_traces = []
    zone_frequency = defaultdict(int)

    for o in outputs:

        # -----------------------------
        # 🔹 SAFE INPUT CHECK
        # -----------------------------
        if not isinstance(o, dict):
            continue

        risk = o.get("risk_level")
        anomaly_score = o.get("anomaly_score", 0)
        trace_id = o.get("trace_id")

        # -----------------------------
        # 🔹 ANOMALY CONDITION
        # -----------------------------
        if risk == "HIGH" or anomaly_score >= 0.6:

            anomaly_count += 1

            # trace tracking
            if trace_id is not None:
                linked_traces.append(str(trace_id))

            # -----------------------------
            # 🔹 SAFE ZONE HANDLING (FIXED)
            # -----------------------------
            lat = o.get("latitude")
            lon = o.get("longitude")

            zone = None

            if isinstance(lat, (int, float)) and isinstance(lon, (int, float)):
                zone = f"{lat}_{lon}"
            else:
                zone = o.get("zone", "Unknown")

            # FORCE SAFE TYPE (IMPORTANT FIX)
            if isinstance(zone, (dict, list, tuple)):
                zone = json_safe_string(zone)

            zone = str(zone)

            affected_zones.add(zone)
            zone_frequency[zone] += 1

    # -----------------------------
    # 🔹 PATTERN ID
    # -----------------------------
    pattern_id = generate_pattern_id(linked_traces)

    # -----------------------------
    # 🔹 SEVERITY
    # -----------------------------
    if anomaly_count >= 5:
        severity_trend = "INCREASING"
        pattern_type = "CLUSTER_ANOMALY"
        summary = "Clustered high-risk anomalies detected in nearby region"

    elif anomaly_count >= 2:
        severity_trend = "STABLE"
        pattern_type = "REPEATED_ANOMALY"
        summary = "Some anomalies detected"

    else:
        severity_trend = "LOW"
        pattern_type = "ISOLATED_EVENT"
        summary = "No major anomalies"

    return {
        "pattern_id": pattern_id,
        "anomaly_count": anomaly_count,
        "affected_zones": sorted(list(affected_zones)),
        "pattern_summary": summary,
        "pattern_type": pattern_type,
        "severity_trend": severity_trend,
        "linked_traces": sorted(linked_traces)
    }


# -----------------------------
# 🔥 WRAPPER
# -----------------------------
def analyze_multi_signals(outputs):
    return analyze_patterns(outputs)


# -----------------------------
# 🔹 SAFE SERIALIZER HELPER (IMPORTANT)
# -----------------------------
def json_safe_string(obj):
    try:
        import json
        return json.dumps(obj, default=str)
    except:
        return str(obj)
