"""
NICAI FULL SYSTEM DEMO
"""

import json

from samachar_input_adapter import load_data, convert_to_signals
from validator import validate_signal
from analytics_engine import analyze_signal
from multi_signal_analyzer import analyze_patterns


def run_demo():

    print("\n==============================")
    print(" NICAI FULL SYSTEM DEMO START ")
    print("==============================\n")

    # STEP 1 — Load datasets
    print("STEP 1 — Loading datasets...\n")

    weather, aqi = load_data()

    print("✅ Datasets loaded successfully\n")

    # STEP 2 — Convert datasets into signals
    print("STEP 2 — Converting datasets into NICAI signals...\n")

    signals = convert_to_signals(weather, aqi)

    print("✅ Total signals generated:", len(signals))

    print("\n------------------------------------")
    print("STEP 3 — Running NICAI Intelligence")
    print("------------------------------------\n")

    processed_outputs = []

    for signal in signals[:20]:

        print("Processing Signal:", signal["signal_id"])

        # VALIDATION
        validation = validate_signal(signal)
        print("VALIDATION:", validation)

        if validation["status"] != "REJECT":

            # ANALYSIS
            analysis = analyze_signal(signal)
            print("ANALYSIS:", analysis)

            # ✅ FIX: include lat/lon for pattern detection
            output = {
                "signal_id": signal["signal_id"],
                "status": validation["status"],
                "confidence_score": validation["confidence_score"],
                "trace_id": validation["trace_id"],
                "anomaly_score": analysis["anomaly_score"],
                "risk_level": analysis["risk_level"],
                "anomaly_type": analysis["anomaly_type"],
                "explanation": analysis["explanation"],
                "recommendation_signal": analysis["recommendation_signal"],

                # ✅ IMPORTANT FIX
                "latitude": signal.get("latitude"),
                "longitude": signal.get("longitude")
            }

            processed_outputs.append(output)

            print("FINAL OUTPUT:", output)

        else:
            print("❌ Signal Rejected")

        print("\n")

    # STEP 4 — Multi Signal Intelligence
    print("------------------------------------")
    print("STEP 4 — Multi-Signal Intelligence")
    print("------------------------------------\n")

    pattern_output = analyze_patterns(processed_outputs)

    print("PATTERN OUTPUT:", pattern_output)

    # Save pattern logs
    with open("pattern_logs.json", "a") as f:
        f.write(json.dumps(pattern_output) + "\n")

    # STEP 5 — Dashboard instructions
    print("\n------------------------------------")
    print("STEP 5 — Launch Dashboard")
    print("------------------------------------\n")

    print("Run this command in a new terminal:\n")
    print("uvicorn dashboard:app --reload\n")   # ✅ FIXED

    print("Then open browser:\n")
    print("http://127.0.0.1:8000\n")           # ✅ FIXED

    print("Dashboard will show:")
    print("• Signals")
    print("• Risk levels")
    print("• Anomaly type")
    print("• Explanation\n")

    # STEP 6 — Action Layer
    print("------------------------------------")
    print("STEP 6 — Trigger Dashboard Actions")
    print("------------------------------------\n")

    print("Click buttons:")
    print("• Escalate")
    print("• Review")
    print("• Assign\n")

    print("These actions will generate structured payloads.\n")

    # STEP 7 — Logs verification
    print("------------------------------------")
    print("STEP 7 — Verify Action Logs")
    print("------------------------------------\n")

    print("Open file:\n")
    print("action_logs.json\n")

    example_log = {
        "trace_id": "...",
        "action_type": "ESCALATE",
        "target_role": "authority",
        "timestamp": "2026-04-14T04:21:32"
    }

    print("Example log entry:\n", example_log)

    print("\n================================")
    print(" NICAI DEMO READY FOR TESTING ")
    print("================================\n")


if __name__ == "__main__":
    run_demo()