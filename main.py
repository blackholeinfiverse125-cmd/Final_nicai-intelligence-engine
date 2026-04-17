from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from datetime import datetime
import json

from validator import validate_signal
from analytics_engine import analyze_signal
from samachar_input_adapter import load_data, convert_to_signals
from error_handler import handle_error
from multi_signal_analyzer import analyze_multi_signals

app = FastAPI()

# -----------------------------
# Templates (Dashboard)
# -----------------------------
templates = Jinja2Templates(directory="templates")


# -----------------------------
# 🔹 Logging Utility (Observability)
# -----------------------------
def log_data(filename, data):
    try:
        with open(filename, "a") as f:
            f.write(json.dumps(data) + "\n")
    except:
        pass


# -----------------------------
# 1️⃣ VALIDATION API
# -----------------------------
@app.post("/validate")
def validate(signal: dict):

    try:
        validation = validate_signal(signal)

        log_data("validation_logs.json", validation)

        return validation

    except Exception as e:
        return handle_error(str(e))


# -----------------------------
# 2️⃣ PIPELINE API (SINGLE SIGNAL)
# -----------------------------
@app.post("/pipeline")
def run_pipeline(signal: dict):

    try:
        validation = validate_signal(signal)

        if validation["status"] == "REJECT":
            return {"validation": validation}

        analytics = analyze_signal(signal)

        return {
            "validation": validation,
            "analytics": analytics
        }

    except Exception as e:
        return handle_error(str(e))


# -----------------------------
# 3️⃣ NICAI FINAL API (INTELLIGENCE ONLY)
# -----------------------------
@app.post("/nicai/evaluate")
def evaluate_signal(signal: dict):

    try:
        # STEP 1: Validation
        validation = validate_signal(signal)

        if validation["status"] == "REJECT":
            return validation

        # STEP 2: Analytics
        analytics = analyze_signal(signal)

        # STEP 3: Recommendation Logic
        if analytics.get("risk") == "HIGH":
            recommendation = "IMMEDIATE_ACTION"
        elif analytics.get("risk") == "MEDIUM":
            recommendation = "MONITOR"
        else:
            recommendation = "SAFE"

        output = {
            "signal_id": validation["signal_id"],
            "status": validation["status"],
            "confidence_score": validation.get("confidence_score", 0.9),
            "trace_id": validation.get("trace_id"),
            "anomaly_score": analytics.get("anomaly_score", 0.5),
            "risk_level": analytics.get("risk", "LOW"),
            "anomaly_type": analytics.get("type", "NORMAL"),
            "explanation": analytics.get("explanation", "No issue"),
            "recommendation_signal": recommendation
        }

        return output

    except Exception as e:
        return handle_error(str(e))


# -----------------------------
# 4️⃣ BATCH RUN (MULTI-SIGNAL)
# -----------------------------
@app.get("/run")
def run_full_pipeline():

    try:
        weather, aqi = load_data()
        signals = convert_to_signals(weather, aqi)

        results = []

        for signal in signals[:50]:

            validation = validate_signal(signal)

            if validation["status"] == "REJECT":
                continue

            analytics = analyze_signal(signal)

            # Recommendation Logic
            if analytics.get("risk") == "HIGH":
                recommendation = "IMMEDIATE_ACTION"
            elif analytics.get("risk") == "MEDIUM":
                recommendation = "MONITOR"
            else:
                recommendation = "SAFE"

            output = {
                "signal_id": signal["signal_id"],
                "status": validation["status"],
                "confidence_score": validation.get("confidence_score", 0.9),
                "trace_id": validation.get("trace_id"),
                "anomaly_score": analytics.get("anomaly_score", 0.5),
                "risk_level": analytics.get("risk", "LOW"),
                "anomaly_type": analytics.get("type", "NORMAL"),
                "explanation": analytics.get("explanation", "No issue"),
                "recommendation_signal": recommendation
            }

            results.append(output)

            # Logging
            log_data("validation_logs.json", validation)

        # Multi-signal intelligence
        summary = analyze_multi_signals(results)

        return {
            "total_processed": len(results),
            "summary": summary,
            "data": results
        }

    except Exception as e:
        return handle_error(str(e))


# -----------------------------
# 5️⃣ DASHBOARD UI 🔥
# -----------------------------
@app.get("/dashboard")
def dashboard(request: Request):

    try:
        weather, aqi = load_data()
        signals = convert_to_signals(weather, aqi)

        results = []

        for signal in signals[:20]:

            validation = validate_signal(signal)

            if validation["status"] == "REJECT":
                continue

            analytics = analyze_signal(signal)

            results.append({
                "signal_id": signal["signal_id"],
                "risk_level": analytics.get("risk"),
                "anomaly_type": analytics.get("type"),
                "explanation": analytics.get("explanation"),
                "trace_id": validation.get("trace_id")
            })

        return templates.TemplateResponse("dashboard.html", {
            "request": request,
            "data": results
        })

    except Exception as e:
        return handle_error(str(e))


# -----------------------------
# 6️⃣ ACTION ROUTING API 🔥
# -----------------------------
@app.post("/action")
def trigger_action(data: dict):

    try:
        action_payload = {
            "trace_id": data.get("trace_id"),
            "action_type": data.get("action_type"),
            "target_role": data.get("target_role", "ADMIN"),
            "timestamp": str(datetime.utcnow()),
            "context": data.get("context", {})
        }

        # Log action
        log_data("action_logs.json", action_payload)

        return {
            "message": "Action generated successfully",
            "action": action_payload
        }

    except Exception as e:
        return handle_error(str(e))