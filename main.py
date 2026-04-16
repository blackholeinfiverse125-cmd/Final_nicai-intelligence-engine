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

templates = Jinja2Templates(directory="templates")


# -----------------------------
# 🔹 SAFE NORMALIZER (IMPORTANT FIX)
# -----------------------------
def normalize_signal(signal):
    """
    Ensures signal is always dict.
    Handles both:
    - dict input
    - JSON string input
    """
    if isinstance(signal, str):
        try:
            return json.loads(signal)
        except Exception:
            raise ValueError("Invalid JSON string provided")
    return signal


# -----------------------------
# 🔹 Logging Utility
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
        signal = normalize_signal(signal)

        validation = validate_signal(signal)
        log_data("validation_logs.json", validation)

        return validation

    except Exception as e:
        return handle_error(str(e))


# -----------------------------
# 2️⃣ PIPELINE API
# -----------------------------
@app.post("/pipeline")
def run_pipeline(signal: dict):

    try:
        signal = normalize_signal(signal)

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
# 3️⃣ NICAI FINAL API
# -----------------------------
@app.post("/nicai/evaluate")
def evaluate_signal(signal: dict):

    try:
        signal = normalize_signal(signal)

        validation = validate_signal(signal)

        if validation["status"] == "REJECT":
            return validation

        analytics = analyze_signal(signal)

        risk = analytics.get("risk", "LOW")

        if risk == "HIGH":
            recommendation = "IMMEDIATE_ACTION"
        elif risk == "MEDIUM":
            recommendation = "MONITOR"
        else:
            recommendation = "SAFE"

        return {
            "signal_id": validation.get("signal_id"),
            "status": validation.get("status"),
            "confidence_score": validation.get("confidence_score", 0.9),
            "trace_id": validation.get("trace_id"),
            "anomaly_score": analytics.get("anomaly_score", 0.5),
            "risk_level": risk,
            "anomaly_type": analytics.get("type", "NORMAL"),
            "explanation": analytics.get("explanation", "No issue"),
            "recommendation_signal": recommendation
        }

    except Exception as e:
        return handle_error(str(e))


# -----------------------------
# 4️⃣ BATCH RUN
# -----------------------------
@app.get("/run")
def run_full_pipeline():

    try:
        weather, aqi = load_data()
        signals = convert_to_signals(weather, aqi)

        results = []

        for signal in signals[:50]:

            try:
                signal = normalize_signal(signal)

                validation = validate_signal(signal)

                if validation["status"] == "REJECT":
                    continue

                analytics = analyze_signal(signal)

                risk = analytics.get("risk", "LOW")

                recommendation = (
                    "IMMEDIATE_ACTION" if risk == "HIGH"
                    else "MONITOR" if risk == "MEDIUM"
                    else "SAFE"
                )

                results.append({
                    "signal_id": signal.get("signal_id"),
                    "status": validation.get("status"),
                    "confidence_score": validation.get("confidence_score", 0.9),
                    "trace_id": validation.get("trace_id"),
                    "anomaly_score": analytics.get("anomaly_score", 0.5),
                    "risk_level": risk,
                    "anomaly_type": analytics.get("type", "NORMAL"),
                    "explanation": analytics.get("explanation", "No issue"),
                    "recommendation_signal": recommendation
                })

                log_data("validation_logs.json", validation)

            except Exception as inner_e:
                log_data("error_logs.json", {"error": str(inner_e)})
                continue

        summary = analyze_multi_signals(results)

        return {
            "total_processed": len(results),
            "summary": summary,
            "data": results
        }

    except Exception as e:
        return handle_error(str(e))


# -----------------------------
# 5️⃣ DASHBOARD
# -----------------------------
@app.get("/dashboard")
def dashboard(request: Request):

    try:
        weather, aqi = load_data()
        signals = convert_to_signals(weather, aqi)

        results = []

        for signal in signals[:20]:

            try:
                signal = normalize_signal(signal)

                validation = validate_signal(signal)

                if validation["status"] == "REJECT":
                    continue

                analytics = analyze_signal(signal)

                results.append({
                    "signal_id": signal.get("signal_id"),
                    "risk_level": analytics.get("risk"),
                    "anomaly_type": analytics.get("type"),
                    "explanation": analytics.get("explanation"),
                    "trace_id": validation.get("trace_id")
                })

            except Exception as inner_e:
                continue

        return templates.TemplateResponse("dashboard.html", {
            "request": request,
            "data": results
        })

    except Exception as e:
        return handle_error(str(e))


# -----------------------------
# 6️⃣ ACTION API
# -----------------------------
@app.post("/action")
def trigger_action(data: dict):

    try:
        data = normalize_signal(data)

        action_payload = {
            "trace_id": data.get("trace_id"),
            "action_type": data.get("action_type"),
            "target_role": data.get("target_role", "ADMIN"),
            "timestamp": str(datetime.utcnow()),
            "context": data.get("context", {})
        }

        log_data("action_logs.json", action_payload)

        return {
            "message": "Action generated successfully",
            "action": action_payload
        }

    except Exception as e:
        return handle_error(str(e))
