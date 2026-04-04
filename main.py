from fastapi import FastAPI
from typing import Union, List
from validator import validate_signal, validate_batch

# Initialize FastAPI app
app = FastAPI(
    title="NICAI Validation Layer", 
    description="Domain-level data integrity validation system",
    version="1.0"
)

# Validation API endpoint
@app.post("/validate")
def validate(data: Union[dict, List[dict]]):

    # Batch processing
    if isinstance(data, list):
        return validate_batch(data)

    # Single signal validation
    return validate_signal(data)
