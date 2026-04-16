import uuid
from collections import defaultdict


def analyze_patterns(outputs):

    anomaly_count = 0
    affected_zones = set()
    linked_traces = []

    zone_frequency = defaultdict(int)

    # loop through signal outputs
    for o in outputs:

        risk = o.get("risk_level")
        trace_id = o.get("trace_id")

        if risk == "HIGH" or o.get("anomaly_score", 0) >= 0.6:

            anomaly_count += 1

            # capture trace ids
            if trace_id:
                linked_traces.append(trace_id)

            # detect zone if available
            lat = o.get("latitude")
            lon = o.get("longitude")

            if lat and lon:
                zone = f"{lat}_{lon}"
            else:
                zone = o.get("zone", "Unknown")

            affected_zones.add(zone)
            zone_frequency[zone] += 1

    # pattern id
    pattern_id = "PATTERN_" + str(uuid.uuid4())[:6]

    # severity trend logic
    if anomaly_count >= 5:
        severity_trend = "INCREASING"
    elif anomaly_count >= 2:
        severity_trend = "STABLE"
    else:
        severity_trend = "LOW"

    # pattern type detection
    if anomaly_count >= 5:
        pattern_type = "CLUSTER_ANOMALY"
    elif anomaly_count >= 2:
        pattern_type = "REPEATED_ANOMALY"
    else:
        pattern_type = "ISOLATED_EVENT"

    # pattern summary
    if anomaly_count >= 5:
        summary = "Clustered high-risk anomalies detected in nearby region"
    elif anomaly_count > 0:
        summary = "Some anomalies detected"
    else:
        summary = "No major anomalies"

    pattern_output = {
        "pattern_id": pattern_id,
        "anomaly_count": anomaly_count,
        "affected_zones": list(affected_zones),
        "pattern_summary": summary,
        "pattern_type": pattern_type,
        "severity_trend": severity_trend,
        "linked_traces": linked_traces
    }

    return pattern_output