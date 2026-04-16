from schemas import required_fields
from dataset_registry import get_dataset
from utils import generate_trace_id, validate_output_schema

import json

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
        
def validate_signal(signal):

    # Generate deterministic trace id
    trace_id = generate_trace_id(signal)

    # 1️⃣ Check missing fields
    for field in required_fields:
        if field not in signal:

            result = {
                "signal_id": signal.get("signal_id"),
                "status": "REJECT",
                "confidence_score": 0.0,
                "trace_id": trace_id,
                "reason": f"missing field {field}"
            }

            validate_output_schema(result)
            emit_bucket_artifact(result)
            emit_telemetry(signal, result)

            return result

    # 2️⃣ Dataset validation
    dataset = get_dataset(signal["dataset_id"])

    if dataset is None:

        result = {
            "signal_id": signal["signal_id"],
            "status": "REJECT",
            "confidence_score": 0.1,
            "trace_id": trace_id,
            "reason": "dataset not registered"
        }

        validate_output_schema(result)
        emit_bucket_artifact(result)
        emit_telemetry(signal, result)

        return result

    # 3️⃣ Dataset inactive
    if dataset["status"] != "active":

        result = {
            "signal_id": signal["signal_id"],
            "status": "FLAG",
            "confidence_score": dataset["trust_score"],
            "trace_id": trace_id,
            "reason": "dataset inactive"
        }

        validate_output_schema(result)
        emit_bucket_artifact(result)
        emit_telemetry(signal, result)

        return result

    # 4️⃣ Valid signal
    result = {
    "signal_id": signal["signal_id"],
    "status": "VALID",
    "confidence_score": dataset["trust_score"],
    "trace_id": trace_id,
    "reason": "valid signal"
}

    validate_output_schema(result)
    emit_bucket_artifact(result)
    emit_telemetry(signal, result)

    return result


def validate_batch(signals):

    # deterministic ordering
    signals = sorted(signals, key=lambda x: x.get("signal_id", ""))

    results = []

    for signal in signals:
        result = validate_signal(signal)
        results.append(result)

    return {"results": results}


def get_validated_signals(signals):
    """
    Returns only ALLOW and FLAG signals
    """

    batch = validate_batch(signals)["results"]

    filtered = []

    for r in batch:
        if r["status"] in ["VALID", "FLAG"]:
            filtered.append(r)

    return filtered
