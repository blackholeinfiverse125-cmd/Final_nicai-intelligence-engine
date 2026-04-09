from fastapi import FastAPI
from validator import validate_signal
from sanskar_stub import analyze_signal
from decision_engine_stub import make_decision

app = FastAPI()

@app.post("/pipeline")
def run_pipeline(signal: dict):

    validation = validate_signal(signal)

    if validation["status"] == "REJECT":
        return {
            "validation": validation,
            "message": "Signal rejected at validation layer"
        }

    analytics = analyze_signal(validation)

    decision = make_decision(analytics)

    return {
        "validation": validation,
        "analytics": analytics,
        "decision": decision
    }