from schemas import required_fields
from dataset_registry import get_dataset
from utils import generate_trace_id

def validate_signal(signal):

    trace_id = generate_trace_id() 

    # Check missing fields
    for field in required_fields:
        if field not in signal:
            return {
                "signal_id": signal.get("signal_id"),
                "status": "REJECT",
                "confidence_score": 0.0,
                "trace_id": trace_id,
                "reason": f"missing field {field}"
            }

    # Dataset check
    dataset = get_dataset(signal["dataset_id"])

    if dataset is None:
        return {
            "signal_id": signal["signal_id"],
            "status": "REJECT",
            "confidence_score": 0.1,
            "trace_id": trace_id,
            "reason": "dataset not registered"
        }

    if dataset["status"] != "active":
        return {
            "signal_id": signal["signal_id"],
            "status": "FLAG",
            "confidence_score": dataset["trust_score"],
            "trace_id": trace_id,
            "reason": "dataset inactive"
        }

    return {
        "signal_id": signal["signal_id"],
        "status": "ALLOW",
        "confidence_score": dataset["trust_score"],
        "trace_id": trace_id,
        "reason": "valid signal"
    }


def validate_batch(signals):

    results = []

    for signal in signals:
        result = validate_signal(signal)
        results.append(result)

    return {"results": results}
