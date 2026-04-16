from schemas import required_fields
from dataset_registry import get_dataset
from utils import generate_trace_id, validate_output_schema
import json


# -----------------------------
# 🔹 SAFE INPUT NORMALIZER
# -----------------------------
def normalize_signal(signal):
    if isinstance(signal, str):
        try:
            signal = json.loads(signal)
        except Exception:
            return None
    return signal


# -----------------------------
# 🔹 LOGGING HELPERS
# -----------------------------
def emit_bucket_artifact(data):
    try:
        with open("bucket_logs.json", "a") as f:
            f.write(json.dumps(data) + "\n")
    except:
        pass


def emit_telemetry(signal, result):
    try:
        with open("telemetry_logs.json", "a") as f:
            f.write(json.dumps({
                "signal": signal,
                "result": result
            }) + "\n")
    except:
        pass


# -----------------------------
# 🔥 CORE VALIDATION ENGINE
# -----------------------------
def validate_signal(signal):

    signal = normalize_signal(signal)

    if not signal:
        return {
            "signal_id": None,
            "status": "REJECT",
            "confidence_score": 0.0,
            "trace_id": None,
            "reason": "invalid signal format"
        }

    trace_id = generate_trace_id(signal)

    signal_id = signal.get("signal_id")

    # -----------------------------
    # 1️⃣ Check required fields
    # -----------------------------
    for field in required_fields:
        if field not in signal:

            result = {
                "signal_id": signal_id,
                "status": "REJECT",
                "confidence_score": 0.0,
                "trace_id": trace_id,
                "reason": f"missing field {field}"
            }

            validate_output_schema(result)
            emit_bucket_artifact(result)
            emit_telemetry(signal, result)

            return result

    # -----------------------------
    # 2️⃣ Dataset validation
    # -----------------------------
    dataset = get_dataset(signal.get("dataset_id"))

    if dataset is None:

        result = {
            "signal_id": signal_id,
            "status": "REJECT",
            "confidence_score": 0.1,
            "trace_id": trace_id,
            "reason": "dataset not registered"
        }

        validate_output_schema(result)
        emit_bucket_artifact(result)
        emit_telemetry(signal, result)

        return result

    # -----------------------------
    # 3️⃣ Dataset inactive
    # -----------------------------
    if dataset.get("status") != "active":

        result = {
            "signal_id": signal_id,
            "status": "FLAG",
            "confidence_score": dataset.get("trust_score", 0.5),
            "trace_id": trace_id,
            "reason": "dataset inactive"
        }

        validate_output_schema(result)
        emit_bucket_artifact(result)
        emit_telemetry(signal, result)

        return result

    # -----------------------------
    # 4️⃣ Valid signal
    # -----------------------------
    result = {
        "signal_id": signal_id,
        "status": "VALID",
        "confidence_score": dataset.get("trust_score", 0.9),
        "trace_id": trace_id,
        "reason": "valid signal"
    }

    validate_output_schema(result)
    emit_bucket_artifact(result)
    emit_telemetry(signal, result)

    return result


# -----------------------------
# 🔥 BATCH VALIDATION
# -----------------------------
def validate_batch(signals):

    if not isinstance(signals, list):
        return {"results": []}

    signals = [
        normalize_signal(s) for s in signals
        if normalize_signal(s) is not None
    ]

    signals = sorted(signals, key=lambda x: x.get("signal_id", ""))

    results = []

    for signal in signals:
        try:
            result = validate_signal(signal)
            results.append(result)
        except Exception as e:
            results.append({
                "signal_id": signal.get("signal_id") if isinstance(signal, dict) else None,
                "status": "REJECT",
                "confidence_score": 0.0,
                "trace_id": None,
                "reason": f"validation error: {str(e)}"
            })

    return {"results": results}


# -----------------------------
# 🔥 FILTERED OUTPUT
# -----------------------------
def get_validated_signals(signals):

    batch = validate_batch(signals)["results"]

    return [
        r for r in batch
        if r.get("status") in ["VALID", "FLAG"]
    ]
