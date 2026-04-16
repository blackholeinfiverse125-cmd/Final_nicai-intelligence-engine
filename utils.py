import hashlib
import json
import os
from jsonschema import validate, ValidationError


def generate_trace_id(signal):
    base_string = f"{signal.get('signal_id','')}|{signal.get('timestamp','')}|{signal.get('dataset_id','')}"
    return hashlib.sha256(base_string.encode()).hexdigest()


def validate_output_schema(output):
    try:
        schema_path = os.path.join(os.path.dirname(__file__), "schema.json")

        with open(schema_path, "r") as f:
            schema = json.load(f)

        validate(instance=output, schema=schema)
        return True

    except ValidationError as e:
        print("Schema validation error:", e)
        return False


def emit_bucket_artifact(data):
    with open("logs.txt", "a") as f:
        f.write(json.dumps(data) + "\n")
