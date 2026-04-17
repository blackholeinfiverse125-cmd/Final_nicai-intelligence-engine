from schemas import required_fields
from dataset_registry import get_dataset
from utils import generate_trace_id, validate_output_schema

# -------------------------------
# SAFE OPTIONAL IMPORTS (OBSERVABILITY)
# -------------------------------
try:
    from bucket_emitter import emit_bucket_artifact
    from telemetry_emitter import emit_telemetry
except ImportError:
    def emit_bucket_artifact(x): pass
    def emit_telemetry(a, b): pass


# -------------------------------
# VALIDATE SINGLE SIGNAL
# -------------------------------
def validate_signal(signal):

    # ✅ deterministic trace id
    trace_id = generate_trace_id(signal)

    # -------------------------------
    # 1️⃣ REQUIRED FIELD CHECK
    # -------------------------------
    for field in required_fields:
        if field not in signal or signal.get(field) in [None, ""]:

            result = {
                "signal_id": signal.get("signal_id"),
                "status": "REJECT",
                "confidence_score": 0.0,
                "trace_id": trace_id,
                "reason": f"missing or empty field: {field}"
            }

            validate_output_schema(result)
            emit_bucket_artifact(result)
            emit_telemetry(signal, result)

            return result

    # -------------------------------
    # 2️⃣ DATASET VALIDATION
    # -------------------------------
    dataset_id = signal.get("dataset_id")
    dataset = get_dataset(dataset_id)

    if dataset is None:

        result = {
            "signal_id": signal.get("signal_id"),
            "status": "REJECT",
            "confidence_score": 0.1,
            "trace_id": trace_id,
            "reason": "dataset not registered"
        }

        validate_output_schema(result)
        emit_bucket_artifact(result)
        emit_telemetry(signal, result)

        return result

    # -------------------------------
    # 3️⃣ DATASET STATUS CHECK
    # -------------------------------
    if dataset.get("status") != "active":

        result = {
            "signal_id": signal.get("signal_id"),
            "status": "FLAG",   # ✅ allowed (not reject)
            "confidence_score": dataset.get("trust_score", 0.5),
            "trace_id": trace_id,
            "reason": "dataset inactive"
        }

        validate_output_schema(result)
        emit_bucket_artifact(result)
        emit_telemetry(signal, result)

        return result

    # -------------------------------
    # 4️⃣ VALID SIGNAL
    # -------------------------------
    result = {
        "signal_id": signal.get("signal_id"),
        "status": "VALID",
        "confidence_score": dataset.get("trust_score", 0.9),
        "trace_id": trace_id,
        "reason": "valid signal"
    }

    validate_output_schema(result)
    emit_bucket_artifact(result)
    emit_telemetry(signal, result)

    return result


# -------------------------------
# VALIDATE BATCH (DETERMINISTIC)
# -------------------------------
def validate_batch(signals):

    # ✅ deterministic ordering
    signals = sorted(signals, key=lambda x: x.get("signal_id", ""))

    results = []

    for signal in signals:
        result = validate_signal(signal)
        results.append(result)

    return {"results": results}


# -------------------------------
# FILTER VALID SIGNALS
# -------------------------------
def get_validated_signals(signals):
    """
    Returns only VALID and FLAG signals
    """

    batch_results = validate_batch(signals)["results"]

    filtered = []

    for r in batch_results:
        if r["status"] in ["VALID", "FLAG"]:
            filtered.append(r)

    return filtered