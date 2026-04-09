# NICAI End-to-End Pipeline Integration – Review Packet

---

# 1. ENTRY POINT

File: main.py

This file exposes the main API endpoint for the NICAI pipeline.

Endpoint:

POST /validate

The API receives structured signals from the upstream system (Samachar / SUM-SCRIPT) and processes them through the full deterministic pipeline.

Pipeline stages:

Input → Validation → Analytics Stub → Decision Stub → API Output

Important Rules Maintained:

• Core validation logic remains unchanged  
• No intelligence logic added to validation  
• No randomness introduced  
• Deterministic processing preserved  

---

# 2. CORE FLOW (MAX 3 FILES)

## validator.py

Responsible for domain-level signal validation.

Responsibilities:

• schema validation  
• required field verification  
• dataset registry lookup  
• status assignment (ALLOW / FLAG / REJECT)  
• deterministic trace_id generation using SHA256  
• bucket artifact emission  
• telemetry emission  

Output Format:

{
 "signal_id": "...",
 "status": "ALLOW / FLAG / REJECT",
 "confidence_score": ...,
 "trace_id": "...",
 "reason": "..."
}

---

## sanskar_stub.py

Acts as the analytics layer stub for integration testing.

Behavior:

• accepts validated signals  
• generates deterministic anomaly score  
• assigns signal priority  

Output Format:

{
 "signal_id": "...",
 "status": "...",
 "confidence_score": ...,
 "anomaly_score": ...,
 "priority": "LOW / MEDIUM / HIGH"
}

No ML or randomness is used.

---

## decision_engine_stub.py

Simulates a rule-based decision layer.

Decision rules:

HIGH anomaly → ALERT  
MEDIUM anomaly → REVIEW  
LOW anomaly → PROCEED  

Output Format:

{
 "decision": "...",
 "risk_level": "...",
 "reason": "Decision based on anomaly score"
}

---

# 3. LIVE FLOW (INPUT → VALIDATION → ANALYTICS → DECISION)

Example Input Signal:

{
 "signal_id": "SIG920",
 "timestamp": "2026-03-10T10:00:00Z",
 "latitude": 19.07,
 "longitude": 72.87,
 "feature_type": "weather",
 "value": 34,
 "dataset_id": "DS01"
}

System Flow:

Samachar Input  
↓  
NICAI Validation Layer  
↓  
Bucket Artifact Emission  
↓  
Telemetry Emission  
↓  
Sanskar Analytics Stub  
↓  
Decision Engine Stub  
↓  
Final API Output

---

Example API Output:

{
 "validation": {
  "signal_id": "SIG920",
  "status": "ALLOW",
  "confidence_score": 0.92,
  "trace_id": "ddcf9985059f61b03c1600f8f6f66ccf8196b176a7bc329a1a7370d6dff75841",
  "reason": "valid signal"
 },

 "analytics": {
  "signal_id": "SIG920",
  "status": "ALLOW",
  "confidence_score": 0.92,
  "anomaly_score": 0.08,
  "priority": "LOW"
 },

 "decision": {
  "decision": "PROCEED",
  "risk_level": "LOW",
  "reason": "Decision based on anomaly score"
 }
}

---

# 4. WHAT WAS BUILT

The NICAI validation module was converted into a **complete deterministic pipeline** ready for integration.

New Components Introduced:

• Sanskar analytics stub  
• Decision engine stub  
• Demo pipeline runner  
• End-to-end API integration  

New Files:

sanskar_stub.py  
decision_engine_stub.py  
run_demo.py  

Capabilities Achieved:

• deterministic pipeline execution  
• validation + analytics + decision integration  
• clean modular architecture  
• full observability preserved  
• demo-ready system flow  

---

# 5. FAILURE CASES HANDLED

The system safely handles the following failure scenarios.

Missing Required Field

Example Output:

{
 "signal_id": null,
 "status": "REJECT",
 "confidence_score": 0.0,
 "trace_id": "...",
 "reason": "missing field signal_id"
}

Behavior:

• pipeline stops after validation  
• analytics and decision layers are skipped  

Dataset Not Registered

Behavior:

• signal rejected  
• structured response returned  

Dataset Inactive

Behavior:

• signal flagged  
• reduced confidence score  

Emitter Failure (Bucket / Telemetry)

Behavior:

• validation still returns output  
• error logged separately  
• system does not crash  

---

# 6. DETERMINISM PROOF

Deterministic trace_id implemented using SHA256 hashing.

Formula:

trace_id = sha256(signal_id + timestamp + dataset_id)

This ensures:

• same input → same trace_id  
• no randomness  
• consistent pipeline behavior  

Repeated executions with identical inputs produced identical outputs.

---

# 7. BATCH CONSISTENCY GUARANTEE

Batch processing ensures deterministic ordering.

Implementation:

signals = sorted(signals, key=lambda x: x["signal_id"])

Guarantees:

• stable output ordering  
• reproducible results across runs  

---

# 8. DEMO PIPELINE EXECUTION

Demo script:

run_demo.py

Command:

python run_demo.py

The script:

• generates sample signals  
• runs full pipeline  
• prints validation, analytics, and decision outputs  

Example Output Structure:

INPUT  
↓  
VALIDATION RESULT  
↓  
ANALYTICS RESULT  
↓  
DECISION RESULT  

This demonstrates the full NICAI pipeline.

---

# 9. HOW TO RUN THE SYSTEM

Step 1 – Install dependencies

pip install fastapi uvicorn

Step 2 – Run validation tests

python test_validation.py

Step 3 – Run demo pipeline

python run_demo.py

Step 4 – Start API server

uvicorn main:app --reload

Step 5 – Open API documentation

http://127.0.0.1:8000/docs

---

# 10. API TESTING

Example Request:

{
 "signal_id": "SIG920",
 "timestamp": "2026-03-10T10:00:00Z",
 "latitude": 19.07,
 "longitude": 72.87,
 "feature_type": "weather",
 "value": 34,
 "dataset_id": "DS01"
}

Example Python API Test:

import requests

url = "http://127.0.0.1:8000/validate"

payload = {
 "signal_id": "SIG920",
 "timestamp": "2026-03-10T10:00:00Z",
 "latitude": 19.07,
 "longitude": 72.87,
 "feature_type": "weather",
 "value": 34,
 "dataset_id": "DS01"
}

response = requests.post(url, json=payload)

print(response.json())

---

# 11. SYSTEM ARCHITECTURE POSITION

Samachar / SUM-SCRIPT (Input Layer)  
↓  
NICAI Validation Layer  
↓  
Bucket Memory Layer  
↓  
InsightFlow Telemetry  
↓  
Sanskar Analytics Layer (Stub)  
↓  
Decision Engine (Stub)  
↓  
Downstream Systems  

The system now functions as a **fully connected deterministic pipeline ready for integration**.

---

# SUMMARY

This implementation converts NICAI from a validation module into a **complete deterministic pipeline system**.

The system guarantees:

• deterministic traceability  
• strict schema validation  
• batch-safe signal processing  
• observability through bucket artifacts and telemetry  
• integration-ready analytics and decision layers  

NICAI is now **demo-ready and integration-ready for downstream intelligence systems**.
