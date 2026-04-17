from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from datetime import datetime
import json

from validator import validate_signal
from analytics_engine import analyze_signal
from samachar_input_adapter import load_data, convert_to_signals
from multi_signal_analyzer import analyze_patterns

app = FastAPI()

# -------------------------------
# LOAD DATA (runs once on startup)
# -------------------------------
weather, aqi = load_data()
signals = convert_to_signals(weather, aqi)


# -------------------------------
# ZONE DETECTION
# -------------------------------
def detect_zone(signal):
    lat = signal.get("latitude")

    if lat is None:
        return "Unknown"

    return "Zone_A" if lat > 20 else "Zone_B"


# -------------------------------
# DASHBOARD ROUTE
# -------------------------------
@app.get("/", response_class=HTMLResponse)
def dashboard():

    rows = ""
    processed_outputs = []

    for signal in signals[:20]:

        validation = validate_signal(signal)

        # 🔴 LOG VALIDATION
        with open("validation_logs.json", "a") as f:
            f.write(json.dumps(validation) + "\n")

        if validation["status"] == "REJECT":
            continue

        analysis = analyze_signal(signal)

        # 🔴 LOG ANALYSIS
        with open("anomaly_logs.json", "a") as f:
            f.write(json.dumps(analysis) + "\n")

        zone = detect_zone(signal)

        output = {
            "signal_id": signal["signal_id"],
            "trace_id": validation["trace_id"],
            "risk_level": analysis["risk_level"],
            "anomaly_score": analysis["anomaly_score"],
            "anomaly_type": analysis["anomaly_type"],
            "zone": zone,
            "latitude": signal.get("latitude"),
            "longitude": signal.get("longitude")
        }

        processed_outputs.append(output)

        rows += f"""
        <tr>
            <td>{signal["signal_id"]}</td>
            <td>{zone}</td>
            <td>{validation["status"]}</td>
            <td>{analysis["risk_level"]}</td>
            <td>{analysis["anomaly_type"]}</td>
            <td>{analysis["explanation"]}</td>

            <td>
                <button onclick="sendAction('{validation["trace_id"]}','ESCALATE','{signal["signal_id"]}','{analysis["risk_level"]}','{analysis["anomaly_type"]}')">Escalate</button>

                <button onclick="sendAction('{validation["trace_id"]}','REVIEW','{signal["signal_id"]}','{analysis["risk_level"]}','{analysis["anomaly_type"]}')">Review</button>

                <button onclick="sendAction('{validation["trace_id"]}','ASSIGN','{signal["signal_id"]}','{analysis["risk_level"]}','{analysis["anomaly_type"]}')">Assign</button>
            </td>
        </tr>
        """

    # -------------------------------
    # PATTERN ANALYSIS
    # -------------------------------
    pattern = analyze_patterns(processed_outputs)

    # 🔴 LOG PATTERN
    with open("pattern_logs.json", "a") as f:
        f.write(json.dumps(pattern) + "\n")

    # -------------------------------
    # OBSERVABILITY
    # -------------------------------
    total_signals = len(signals)

    total_anomalies = len(
        [o for o in processed_outputs if o["risk_level"] != "LOW"]
    )

    total_patterns = 1 if pattern["anomaly_count"] > 0 else 0

    # action log count
    try:
        with open("action_logs.json") as f:
            action_count = len(f.readlines())
    except:
        action_count = 0

    # -------------------------------
    # HTML TEMPLATE
    # -------------------------------
    html = f"""
    <html>
    <head>
        <title>NICAI Intelligence Dashboard</title>

        <script>
        async function sendAction(trace_id, action_type, signal_id, risk_level, anomaly_type) {{

            const response = await fetch("/action", {{
                method: "POST",
                headers: {{
                    "Content-Type": "application/json"
                }},
                body: JSON.stringify({{
                    trace_id: trace_id,
                    action_type: action_type,
                    context: {{
                        signal_id: signal_id,
                        risk_level: risk_level,
                        anomaly_type: anomaly_type
                    }}
                }})
            }});

            const data = await response.json();
            alert("Action Sent: " + JSON.stringify(data));
        }}
        </script>

    </head>

    <body>

        <h2>NICAI Intelligence Dashboard</h2>

        <h3>System Observability</h3>
        <table border="1" cellpadding="6">
            <tr>
                <th>Total Signals</th>
                <th>Total Anomalies</th>
                <th>Patterns Detected</th>
                <th>Actions Logged</th>
            </tr>
            <tr>
                <td>{total_signals}</td>
                <td>{total_anomalies}</td>
                <td>{total_patterns}</td>
                <td>{action_count}</td>
            </tr>
        </table>

        <br>

        <h3>Observability Logs</h3>
        <ul>
            <li>Validation logs → validation_logs.json</li>
            <li>Anomaly logs → anomaly_logs.json</li>
            <li>Pattern logs → pattern_logs.json</li>
            <li>Action logs → action_logs.json</li>
        </ul>

        <br>

        <h3>Pattern Summary</h3>
        <table border="1" cellpadding="6">
            <tr>
                <th>Pattern ID</th>
                <th>Anomaly Count</th>
                <th>Pattern Type</th>
                <th>Severity Trend</th>
            </tr>
            <tr>
                <td>{pattern["pattern_id"]}</td>
                <td>{pattern["anomaly_count"]}</td>
                <td>{pattern["pattern_type"]}</td>
                <td>{pattern["severity_trend"]}</td>
            </tr>
        </table>

        <br>

        <h3>Signals</h3>

        <table border="1" cellpadding="8">

            <tr>
                <th>Signal ID</th>
                <th>Zone</th>
                <th>Status</th>
                <th>Risk Level</th>
                <th>Anomaly Type</th>
                <th>Explanation</th>
                <th>Action</th>
            </tr>

            {rows}

        </table>

    </body>
    </html>
    """

    return HTMLResponse(content=html)


# -------------------------------
# API: SIGNALS
# -------------------------------
@app.get("/signals")
def get_signals():

    processed = []

    for signal in signals[:20]:
        validation = validate_signal(signal)

        if validation["status"] == "REJECT":
            continue

        analysis = analyze_signal(signal)

        processed.append({
            "signal_id": signal["signal_id"],
            "status": validation["status"],
            "risk_level": analysis["risk_level"],
            "anomaly_type": analysis["anomaly_type"],
            "trace_id": validation["trace_id"]
        })

    return {"signals": processed}


# -------------------------------
# API: PATTERNS
# -------------------------------
@app.get("/patterns")
def get_patterns():

    processed_outputs = []

    for signal in signals[:20]:
        validation = validate_signal(signal)

        if validation["status"] == "REJECT":
            continue

        analysis = analyze_signal(signal)

        processed_outputs.append({
            "trace_id": validation["trace_id"],
            "risk_level": analysis["risk_level"],
            "anomaly_score": analysis["anomaly_score"],
            "zone": detect_zone(signal),
            "latitude": signal.get("latitude"),
            "longitude": signal.get("longitude")
        })

    pattern = analyze_patterns(processed_outputs)

    return pattern


# -------------------------------
# ACTION ROUTING
# -------------------------------
@app.post("/action")
async def action_router(payload: dict):

    action_payload = {
        "trace_id": payload["trace_id"],
        "action_type": payload["action_type"],
        "target_role": "authority",
        "timestamp": str(datetime.utcnow()),
        "context": payload.get("context", {})  # ✅ FIXED
    }

    with open("action_logs.json", "a") as f:
        f.write(json.dumps(action_payload) + "\n")

    return {
        "status": "action logged",
        "payload": action_payload
    }