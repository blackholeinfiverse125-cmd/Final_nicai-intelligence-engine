import json
from datetime import datetime

BUCKET_FILE = "bucket_artifacts.jsonl"


def emit_bucket_artifact(validation_output):

    artifact = {
        "trace_id": validation_output["trace_id"],
        "signal_id": validation_output["signal_id"],
        "status": validation_output["status"],
        "confidence_score": validation_output["confidence_score"],
        "reason": validation_output["reason"],
        "timestamp": datetime.utcnow().isoformat(),
        "layer": "NICAI_VALIDATION"
    }

    try:
        with open(BUCKET_FILE, "a", encoding="utf-8") as f:
            f.write(json.dumps(artifact) + "\n")

    except Exception as e:
        print("Bucket emission failed:", e)