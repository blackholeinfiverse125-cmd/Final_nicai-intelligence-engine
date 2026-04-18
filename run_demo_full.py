"""
NICAI FULL SYSTEM DEMO (FINAL - STABLE & TANTRA ALIGNED)
"""

import json
from datetime import datetime, timezone

from samachar_input_adapter import load_data, convert_to_signals
from validator import validate_signal
from sanskar_engine import analyze_signal, analyze_patterns
from error_handler import error_response, validate_basic_input


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
            f.write(json.dumps(log_entry) + "\n")

    except Exception:
        pass


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

        # ✅ STRICT INPUT VALIDATION
        error = validate_basic_input(signals)
        if error:
            print("❌ INPUT ERROR:", error)
            return

        print(f"✅ Total signals: {len(signals)}\n")

        # -----------------------------
        # STEP 3 — Process signals
        # -----------------------------
        print("------------------------------------")
        print("STEP 3 — Running Intelligence")
        print("------------------------------------\n")

        processed_outputs = []

        low = medium = high = 0

        for signal in signals[:20]:

            # -----------------------------
            # VALIDATION
            # -----------------------------
            validation = validate_signal(signal)

            if validation.get("status") == "ERROR":
                continue

            log_data("validation_logs.json", "VALIDATION", validation)

            # -----------------------------
            # ANALYSIS
            # -----------------------------
            analysis = analyze_signal(signal)

            if isinstance(analysis, dict) and analysis.get("status") == "ERROR":
                continue

            # -----------------------------
            # 🔥 TANTRA SAFE RECOMMENDATION (FIX)
            # -----------------------------
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

            # -----------------------------
            # SUMMARY COUNTS
            # -----------------------------
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
        # STEP 5 — Dashboard
        # -----------------------------
        print("\n------------------------------------")
        print("STEP 5 — Launch Dashboard")
        print("------------------------------------\n")

        print("Run in new terminal:")
        print("uvicorn main:app --reload\n")

        print("Open browser:")
        print("http://127.0.0.1:8000/dashboard\n")

        # -----------------------------
        # STEP 6 — Actions
        # -----------------------------
        print("------------------------------------")
        print("STEP 6 — Trigger Actions")
        print("------------------------------------\n")

        print("Use buttons:")
        print("• eligible_for_escalation")
        print("• requires_review")
        print("• monitor\n")

        # -----------------------------
        # STEP 7 — Logs
        # -----------------------------
        print("------------------------------------")
        print("STEP 7 — Verify Logs")
        print("------------------------------------\n")

        print("Check file: logs/action_logs.json\n")

        example_log = {
            "trace_id": "...",
            "action_type": "eligible_for_escalation",
            "target_role": "authority",
            "timestamp": datetime.now(timezone.utc).isoformat()
        }

        print("Example log:")
        print(example_log)

        # -----------------------------
        # STEP 8 — TRACE CONTINUITY
        # -----------------------------
        print("\n------------------------------------")
        print("STEP 8 — Trace ID Continuity")
        print("------------------------------------\n")

        if processed_outputs:
            print("Sample trace_id:", processed_outputs[0].get("trace_id"))
            print("Trace ID flows across validation → analytics → action logs\n")

        print("\n================================")
        print(" NICAI DEMO READY ")
        print("================================\n")

    except Exception as e:
        print("❌ DEMO ERROR:", error_response(str(e)))


if __name__ == "__main__":
    run_demo()