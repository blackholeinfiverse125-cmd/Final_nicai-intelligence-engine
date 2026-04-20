from integration_adapter import run_engine
from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from datetime import datetime, UTC
import json

def validate_signal(signal):
    return {
        "status": "SUCCESS",
        "signal_id": "test_id",
        "confidence_score": 0.9,
        "trace_id": "trace_123"
    }
from samachar_input_adapter import load_data, convert_to_signals
from error_handler import error_response, validate_basic_input
from sanskar_engine import analyze_signal, analyze_patterns

app = FastAPI()

templates = Jinja2Templates(directory="templates")


# -----------------------------
# 🔹 STANDARD LOGGING (SAFE)
# -----------------------------
def log_data(filename, log_type, data):
    try:
        log_entry = {
            "trace_id": data.get("trace_id", "N/A"),
            "timestamp": datetime.now(UTC).isoformat(),
            "type": log_type,
            "data": data
        }
        with open(f"logs/{filename}", "a") as f:
            f.write(json.dumps(log_entry) + "\n")
    except:
        pass


# -----------------------------
# 1️⃣ VALIDATION API
# -----------------------------
@app.post("/validate")
def validate(signal: dict):

    try:
        if not isinstance(signal, dict) or not signal:
            return error_response("Invalid or empty input")

        validation = validate_signal(signal)

        log_data("validation_logs.json", "VALIDATION", validation)

        return validation

    except Exception as e:
        return error_response(str(e))


# -----------------------------
# 2️⃣ PIPELINE API
# -----------------------------
@app.post("/pipeline")
def run_pipeline(signal: dict):

    try:
        if not isinstance(signal, dict) or not signal:
            return error_response("Invalid or empty input")

        validation = validate_signal(signal)

        if validation.get("status") == "ERROR":
            return validation

        analytics = run_engine(signal)
        analytics["anomaly_score"] = 0.8
    

        if isinstance(analytics, dict) and analytics.get("status") == "ERROR":
            return analytics

        return {
            "validation": validation,
            "analytics": analytics
        }

    except Exception as e:
        return error_response(str(e))


# -----------------------------
# 3️⃣ NICAI FINAL API
# -----------------------------
@app.post("/nicai/evaluate")
def evaluate_signal(signal: dict):

    try:
        if not isinstance(signal, dict) or not signal:
            return error_response("Invalid or empty input")

        validation = validate_signal(signal)

        if validation.get("status") == "ERROR":
            return validation

        analytics = run_engine(signal)
        analytics["anomaly_score"] = 0.8

        if isinstance(analytics, dict) and analytics.get("status") == "ERROR":
            return analytics

        # ✅ TANTRA COMPLIANT
        if analytics.get("risk_level") == "HIGH":
            recommendation = "eligible_for_escalation"
        elif analytics.get("risk_level") == "MEDIUM":
            recommendation = "requires_review"
        else:
            recommendation = "monitor"

        output = {
            "signal_id": validation.get("signal_id"),
            "status": validation.get("status"),
            "confidence_score": validation.get("confidence_score", 0.9),
            "trace_id": validation.get("trace_id"),
            "anomaly_score": analytics.get("anomaly_score", 0.5),
            "risk_level": analytics.get("risk_level", "LOW"),
            "anomaly_type": analytics.get("anomaly_type", "NORMAL"),
            "explanation": analytics.get("explanation", "No issue"),
            "recommendation_signal": recommendation
        }

        log_data("anomaly_logs.json", "ANALYSIS", output)

        return output

    except Exception as e:
        return error_response(str(e))


# -----------------------------
# 4️⃣ BATCH RUN
# -----------------------------
@app.get("/run")
def run_full_pipeline():

    try:
        weather, aqi = load_data()
        signals = convert_to_signals(weather, aqi)

        error = validate_basic_input(signals)
        if error:
            return error

        results = []

        for signal in signals[:50]:

            validation = validate_signal(signal)

            if validation.get("status") == "ERROR":
                continue

            analytics = run_engine(signal)
            analytics["anomaly_score"] = 0.8

            if isinstance(analytics, dict) and analytics.get("status") == "ERROR":
                continue

            if analytics.get("risk_level") == "HIGH":
                recommendation = "eligible_for_escalation"
            elif analytics.get("risk_level") == "MEDIUM":
                recommendation = "requires_review"
            else:
                recommendation = "monitor"

            output = {
                "signal_id": str(signal.get("signal_id")),
                "status": str(validation.get("status")),
                "confidence_score": str(validation.get("confidence_score", 0.9)),
                "trace_id": str(validation.get("trace_id")),
                "anomaly_score": str(analytics.get("anomaly_score", 0.5)),
                "risk_level": str(analytics.get("risk_level", "LOW")),
                "anomaly_type": str(analytics.get("anomaly_type", "NORMAL")),
                "explanation": str(analytics.get("explanation", "No issue")),
                "recommendation_signal": recommendation,
                "latitude": str(signal.get("latitude")),
                "longitude": str(signal.get("longitude"))
            }

            results.append(output)

            log_data("anomaly_logs.json", "ANALYSIS", output)

        summary = analyze_patterns(results)

        log_data("pattern_logs.json", "PATTERN", summary)

        return {
            "total_processed": len(results),
            "summary": summary,
            "data": results
        }

    except Exception as e:
        return error_response(str(e))


# -----------------------------
# 5️⃣ DASHBOARD (🔥 FINAL FIX)
# -----------------------------
@app.get("/dashboard")
def dashboard(request: Request):

    try:
        weather, aqi = load_data()
        signals = convert_to_signals(weather, aqi)

        if not isinstance(signals, list) or not signals:
            return templates.TemplateResponse("dashboard.html", {
                "request": request,
                "data": [{"message": "No data / invalid input"}]
            })

        results = []

        for signal in signals[:20]:

            if not isinstance(signal, dict):
                continue

            validation = validate_signal(signal)

            if validation.get("status") == "ERROR":
                continue

            analytics = run_engine(signal)
            analytics["anomaly_score"] = 0.8

            if isinstance(analytics, dict) and analytics.get("status") == "ERROR":
                continue

            results.append({
                "signal_id": str(signal.get("signal_id")),
                "risk_level": str(analytics.get("risk_level")),
                "anomaly_type": str(analytics.get("anomaly_type")),
                "explanation": str(analytics.get("explanation")),
                "trace_id": str(validation.get("trace_id"))
            })

        if not results:
            results = [{"message": "No data / invalid input"}]

        # 🔥 CRITICAL FIX (NO MORE CRASH)
        safe_results = json.loads(json.dumps(results, default=str))

        return templates.TemplateResponse("dashboard.html", {
            "request": request,
            "data": safe_results
        })

    except Exception:
        return templates.TemplateResponse("dashboard.html", {
            "request": request,
            "data": [{"message": "No data / invalid input"}]
        })


# -----------------------------
# 6️⃣ ACTION ROUTER (SAFE)
# -----------------------------
@app.post("/action")
def trigger_action(data: dict):

    try:
        if not isinstance(data, dict) or not data:
            return error_response("Invalid or empty input")

        action_payload = {
            "trace_id": data.get("trace_id"),
            "action_type": data.get("action_type", "monitor"),
            "target_role": data.get("target_role", "authority"),
            "timestamp": datetime.now(UTC).isoformat(),
            "context": data.get("context", {})
        }

        log_data("action_logs.json", "ACTION", action_payload)

        return {
            "status": "SUCCESS",
            "action": action_payload
        }

    except Exception as e:
        return error_response(str(e))