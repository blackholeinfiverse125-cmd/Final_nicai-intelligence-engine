"""
NICAI FULL SYSTEM DEMO (FINAL - STABLE + FAILURE SAFE + SINGLE COMMAND)
"""

import json
import os
from datetime import datetime, timezone

from samachar_input_adapter import load_data, convert_to_signals
from validator import validate_signal
from sanskar_engine import analyze_signal, analyze_patterns
from error_handler import error_response, validate_basic_input


# -----------------------------
# ✅ ENSURE REQUIRED FOLDERS
# -----------------------------
os.makedirs("logs", exist_ok=True)
os.makedirs("data", exist_ok=True)


# -----------------------------
# STANDARD LOGGING (SAFE)
# -----------------------------
def log_data(filename, log_type, data):
    try:
        log_entry = {
            "trace_id": data.get("trace_id", "N/A"),
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "type": log_type,
            "data": data
        }

        with open(f"logs/{filename}", "a") as f:
            f.write(json.dumps(log_entry, default=str) + "\n")

    except Exception:
        pass


# -----------------------------
# DEMO RUNNER
# -----------------------------
def run_demo():

    print("\n==============================")
    print(" NICAI FULL SYSTEM DEMO START ")
    print("==============================\n")

    try:
        # -----------------------------
        # STEP 1 — Load datasets
        # -----------------------------
        print("STEP 1 — Loading datasets...\n")

        weather, aqi = load_data()
        print("✅ Datasets loaded successfully\n")

        # -----------------------------
        # STEP 2 — Convert to signals
        # -----------------------------
        print("STEP 2 — Converting to signals...\n")

        signals = convert_to_signals(weather, aqi)

        # ✅ HARD INPUT GATE
        error = validate_basic_input(signals)
        if error:
            print(json.dumps(error, indent=2))
            return

        print(f"✅ Total signals: {len(signals)}\n")

        # -----------------------------
        # STEP 3 — Processing
        # -----------------------------
        print("------------------------------------")
        print("STEP 3 — Running Intelligence")
        print("------------------------------------\n")

        processed_outputs = []

        low = medium = high = 0

        for signal in signals[:20]:

            if not isinstance(signal, dict):
                continue

            # VALIDATION
            validation = validate_signal(signal)
            if validation is None:
                continue
            
            if validation.get("status") == "ERROR":
                continue

            log_data("validation_logs.json", "VALIDATION", validation)

            # ANALYSIS
            analysis = analyze_signal(signal)

            if not isinstance(analysis, dict) or analysis.get("status") == "ERROR":
                continue

            # ✅ TANTRA SAFE OUTPUT
            if analysis.get("risk_level") == "HIGH":
                recommendation = "eligible_for_escalation"
            elif analysis.get("risk_level") == "MEDIUM":
                recommendation = "requires_review"
            else:
                recommendation = "monitor"

            output = {
                "signal_id": signal.get("signal_id"),
                "trace_id": validation.get("trace_id"),
                "risk_level": analysis.get("risk_level"),
                "anomaly_score": analysis.get("anomaly_score"),
                "anomaly_type": analysis.get("anomaly_type"),
                "recommendation_signal": recommendation,
                "latitude": signal.get("latitude"),
                "longitude": signal.get("longitude")
            }

            processed_outputs.append(output)

            # SUMMARY
            if output["risk_level"] == "LOW":
                low += 1
            elif output["risk_level"] == "MEDIUM":
                medium += 1
            elif output["risk_level"] == "HIGH":
                high += 1

            log_data("anomaly_logs.json", "ANALYSIS", output)

        print("✅ Processing complete\n")

        # -----------------------------
        # SUMMARY
        # -----------------------------
        print("📊 SUMMARY:")
        print(f"LOW: {low}")
        print(f"MEDIUM: {medium}")
        print(f"HIGH: {high}\n")

        # -----------------------------
        # STEP 4 — Pattern Detection
        # -----------------------------
        print("------------------------------------")
        print("STEP 4 — Pattern Detection")
        print("------------------------------------\n")

        if not processed_outputs:
            pattern_output = {
                "pattern_id": "PATTERN_NONE",
                "anomaly_count": 0,
                "affected_zones": [],
                "pattern_summary": "No data available",
                "pattern_type": "NO_PATTERN",
                "severity_trend": "NONE",
                "linked_traces": []
            }
        else:
            pattern_output = analyze_patterns(processed_outputs)

        print("PATTERN:", pattern_output)

        log_data("pattern_logs.json", "PATTERN", pattern_output)

        # -----------------------------
        # STEP 5 — AUTO START API 🔥
        # -----------------------------
        print("\n------------------------------------")
        print("STEP 5 — Starting Dashboard (AUTO)")
        print("------------------------------------\n")

        print("🚀 Launching API server...")

        # 🔥 SINGLE COMMAND FIX
        os.system("uvicorn main:app --reload")

        # -----------------------------
        # STEP 6 — Instructions
        # -----------------------------
        print("\nOpen browser:")
        print("http://127.0.0.1:8000/dashboard\n")

        print("Actions:")
        print("• eligible_for_escalation")
        print("• requires_review")
        print("• monitor\n")

        print("Check logs:")
        print("logs/action_logs.json\n")

        # TRACE
        if processed_outputs:
            print("Sample trace_id:", processed_outputs[0].get("trace_id"))

        print("\n================================")
        print(" NICAI DEMO READY ")
        print("================================\n")

    except Exception as e:
        print(json.dumps(error_response(str(e)), indent=2))


# -----------------------------
# ENTRY POINT
# -----------------------------
if __name__ == "__main__":
    run_demo()
