import hashlib
import json
from jsonschema import validate


def generate_trace_id(signal):
    """
    Generate deterministic trace_id using SHA256.

    Same input → same trace_id.
    Handles malformed inputs safely.
    """

    signal_id = str(signal.get("signal_id", "unknown"))
    timestamp = str(signal.get("timestamp", "unknown"))
    dataset_id = str(signal.get("dataset_id", "unknown"))

    base_string = f"{signal_id}{timestamp}{dataset_id}"

    trace_id = hashlib.sha256(base_string.encode()).hexdigest()

    return trace_id


def validate_output_schema(output):
    """
    Enforce strict validation output contract using schema.json.
    Ensures no schema drift across systems.
    """

    with open("schema.json", "r") as f:
        schema = json.load(f)

    validate(instance=output, schema=schema)