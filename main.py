from fastapi import FastAPI
from validator import validate_signal
from analytics_engine import analyze_signal
from decision_engine import make_decision
from samachar_input_adapter import adapt_input
from error_handler import handle_error

app = FastAPI()


# -----------------------------
# 1️⃣ VALIDATION API
# -----------------------------
@app.post("/validate")
def validate(signal: dict):

    try:
        signal = adapt_input(signal)
        validation = validate_signal(signal)
        return validation

    except Exception as e:
        return handle_error(str(e))


# -----------------------------
# 2️⃣ PIPELINE API
# -----------------------------
@app.post("/pipeline")
def run_pipeline(signal: dict):

    try:
        signal = adapt_input(signal)

        validation = validate_signal(signal)

        if validation["status"] == "REJECT":
            return {"validation": validation}

        analytics = analyze_signal(validation)
        decision = make_decision(analytics)

        return {
            "validation": validation,
            "analytics": analytics,
            "decision": decision
        }

    except Exception as e:
        return handle_error(str(e))


# -----------------------------
# 3️⃣ NICAI FINAL API
# -----------------------------
@app.post("/nicai/evaluate")
def evaluate_signal(signal: dict):

    try:
        signal = adapt_input(signal)

        validation = validate_signal(signal)

        if validation["status"] == "REJECT":
            return validation

        analytics = analyze_signal(validation)
        decision = make_decision(analytics)

        return {
            "signal_id": validation["signal_id"],
            "status": validation["status"],
            "confidence_score": validation["confidence_score"],
            "trace_id": validation["trace_id"],
            "reason": validation["reason"],
            "anomaly_score": analytics["anomaly_score"],
            "priority": analytics["priority"],
            "decision": decision["decision"],
            "risk_level": decision["risk_level"],
            "summary_line": f"Signal {decision['decision']} with {analytics['priority']} priority",
            "explanation": decision["reason"]
        }

    except Exception as e:
        return handle_error(str(e))