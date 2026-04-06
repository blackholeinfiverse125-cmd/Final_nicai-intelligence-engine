import uuid
import json
from jsonschema import validate

# Load validation output schema
with open("schema.json") as f:
    validation_schema = json.load(f)


def generate_trace_id():
    """
    Generates a unique trace identifier for each signal validation.
    """
    return str(uuid.uuid4())


def validate_output_schema(output):
    """
    Ensures validation output follows the fixed schema contract.
    Prevents schema drift across systems.
    """
    validate(instance=output, schema=validation_schema)
