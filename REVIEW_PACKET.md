# NICAI Observability & Contract Layer – Review Packet

---

# 1. ENTRY POINT

**File:** `main.py`

This file is the entry point of the NICAI validation system and exposes the API endpoint:

POST /validate

The endpoint receives structured signals from the upstream system (SUM-SCRIPT / Samachar) and forwards them to the validation logic.

Supported modes:

• Single signal validation  
• Batch signal validation  

The system performs **data integrity validation only**.

The validation layer **does NOT**:

• enforce governance decisions  
• block pipeline execution  
• modify downstream behavior  

It only ensures that signals entering the intelligence system are **clean, structured, and traceable**.

---

# 2. CORE FLOW (MAX 3 FILES)

## validator.py

Contains the core signal validation logic.

Responsibilities:

• validate signal schema  
• check required fields  
• verify dataset registry  
• assign validation status (ALLOW / FLAG / REJECT)  
• generate trace identifiers  
• produce deterministic validation outputs  

Each signal is processed **independently**, ensuring safe batch processing.

---

## bucket_emitter.py

This module emits validation artifacts to the **Bucket Memory Layer**.

For each validated signal, the system generates an artifact:

```
{
 "trace_id": "...",
 "signal_id": "...",
 "status": "...",
 "confidence_score": ...,
 "reason": "...",
 "timestamp": "...",
 "layer": "NICAI_VALIDATION"
}
```

Artifacts are written to:

```
bucket_artifacts.jsonl
```

Purpose:

• provide traceable validation history  
• ensure compatibility with memory systems  
• enable system debugging and lineage tracking

---

## telemetry_emitter.py

Responsible for **system observability and telemetry emission**.

Telemetry generated per signal:

```
{
 "trace_id": "...",
 "dataset_id": "...",
 "status": "...",
 "confidence_score": ...,
 "timestamp": "..."
}
```

Metrics monitored:

• total signals processed  
• reject rate  
• flag rate  
• dataset mismatch rate  
• confidence score distribution  

Telemetry records are stored in:

```
telemetry.log
```

Purpose:

• system monitoring  
• validation performance tracking  
• operational visibility

---

# 3. LIVE FLOW (INPUT → VALIDATION → BUCKET → TELEMETRY)

### Example Input Signal (Upstream System)

```json
{
 "signal_id": "SIG910",
 "timestamp": "2026-03-10T10:00:00Z",
 "latitude": 19.07,
 "longitude": 72.87,
 "feature_type": "weather",
 "value": 34,
 "dataset_id": "DS01"
}
```

---

### System Processing Flow

```
Upstream Input (SUM-SCRIPT / Samachar)
              ↓
NICAI Validation Layer
              ↓
Schema Validation
              ↓
Dataset Registry Verification
              ↓
Validation Output Generated
              ↓
Bucket Artifact Emission
              ↓
Telemetry Metrics Emission
```

---

### Example Validation Output

```json
{
 "signal_id": "SIG910",
 "status": "ALLOW",
 "confidence_score": 0.92,
 "trace_id": "615fd90b-999c-4d87-8815-45628ba88ff5",
 "reason": "valid signal"
}
```

---

### Example Bucket Artifact

```
{
 "trace_id": "615fd90b-999c-4d87-8815-45628ba88ff5",
 "signal_id": "SIG910",
 "status": "ALLOW",
 "confidence_score": 0.92,
 "reason": "valid signal",
 "timestamp": "2026-04-06T05:21:55",
 "layer": "NICAI_VALIDATION"
}
```

---

### Example Telemetry Record

```
{
 "trace_id": "615fd90b-999c-4d87-8815-45628ba88ff5",
 "dataset_id": "DS01",
 "status": "ALLOW",
 "confidence_score": 0.92,
 "timestamp": "2026-04-06T05:21:55"
}
```

---

# 4. WHAT WAS BUILT

The validation system was upgraded into a **fully observable domain-level data integrity layer**.

### New Capabilities

• Bucket artifact emission (memory compatibility)  
• Telemetry emission (system observability)  
• strict validation output contract  
• deterministic validation outputs  
• structured schema enforcement  
• compatibility with analytics systems

### New Modules Introduced

```
bucket_emitter.py
telemetry_emitter.py
schema.json
```

The existing validation logic was **not modified**, ensuring system stability.

---

# 5. FAILURE CASES HANDLED

The system safely handles multiple failure scenarios.

### Missing Field

Example failure output:

```json
{
 "signal_id": null,
 "status": "REJECT",
 "confidence_score": 0.0,
 "trace_id": "generated_uuid",
 "reason": "missing field signal_id"
}
```

---

### Dataset Not Registered

Behavior:

• signal rejected  
• structured response returned  

---

### Dataset Inactive

Behavior:

• signal flagged  
• reduced confidence score  

---

### Emitter Failure

If Bucket or Telemetry emission fails:

• validation result still returned  
• failure logged separately  
• system does not crash

---

# 6. DETERMINISM PROOF

The validation system was tested using repeated executions of identical inputs.

Observations:

• validation outputs remained consistent  
• schema validation produced identical results  
• telemetry and bucket emissions were stable  

Trace IDs are generated using UUID to ensure **global traceability across systems**.

---

# 7. PROOF (TESTING)

Validation testing was performed using **two methods**.

---

## Script Testing

Test file:

```
test_validation.py
```

Command executed:

```
python test_validation.py
```

Test scenarios:

• valid signal validation  
• inactive dataset validation  
• missing field validation  
• malformed input validation  
• batch signal validation

---

## API Testing

Server started using:

```
uvicorn main:app --reload
```

API documentation:

```
http://127.0.0.1:8000/docs
```

Endpoint tested:

```
POST /validate
```

---

### API Testing Python Script

Example API testing code:

```python
import requests

url = "http://127.0.0.1:8000/validate"

payload = [
 {
  "signal_id": "SIG910",
  "timestamp": "2026-03-10T10:00:00Z",
  "latitude": 19.07,
  "longitude": 72.87,
  "feature_type": "weather",
  "value": 34,
  "dataset_id": "DS01"
 },
 {
  "signal_id": "SIG911",
  "timestamp": "2026-03-10T10:05:00Z",
  "latitude": 18.52,
  "longitude": 73.85,
  "feature_type": "vessel",
  "value": 120,
  "dataset_id": "DS02"
 }
]

response = requests.post(url, json=payload)

print(response.json())
```

Expected output:

```
{
 "results": [
  {
   "signal_id": "SIG910",
   "status": "ALLOW",
   "confidence_score": 0.92,
   "trace_id": "...",
   "reason": "valid signal"
  },
  {
   "signal_id": "SIG911",
   "status": "FLAG",
   "confidence_score": 0.45,
   "trace_id": "...",
   "reason": "dataset inactive"
  }
 ]
}
```

---

# 8. SYSTEM ARCHITECTURE POSITION

```
SUM-SCRIPT / Samachar (Structured Input)
              ↓
NICAI Validation Layer
              ↓
Bucket (Memory Layer)
              ↓
InsightFlow (Observability)
              ↓
Sanskar (Analytics)
              ↓
Chayan (Agent Selection)
              ↓
Sūtradhāra (Contract Builder)
              ↓
RAJYA / SAARTHI Systems
```

NICAI now functions as an **observable domain data integrity layer ready for TANTRA integration**.

---

# SUMMARY

This implementation upgrades the NICAI validation system into a **fully observable data integrity layer**.

The system guarantees:

• schema-safe validation  
• deterministic outputs  
• traceable validation artifacts  
• telemetry-based observability  
• compatibility with analytics and intelligence systems  

The system is now **TANTRA-ready and SVACS-compatible**.
