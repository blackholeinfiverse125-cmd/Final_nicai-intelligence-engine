# NICAI Deterministic Validation & Observability Layer

This project implements the **NICAI Domain Data Integrity, Observability, and Deterministic Validation Layer**.

The system validates incoming signals and ensures that they are **clean, traceable, deterministic, and ready for downstream intelligence systems**.

The validation layer performs **data integrity validation only** and does **not enforce decisions or block pipeline execution**.

---

# Project Objective

The objective of this system is to create a **deterministic and contract-safe validation boundary inside the NICAI intelligence pipeline**.

The system guarantees that:

• incoming signals follow a strict schema  
• dataset registry validation is enforced  
• trace identifiers are deterministic  
• validation artifacts are stored for memory systems  
• telemetry metrics are emitted for observability  
• downstream systems receive contract-safe outputs  

The validation layer prepares **trusted signals for analytics and intelligence systems**.

---

# System Architecture

```
SUM-SCRIPT / Samachar (Structured Input)
              ↓
NICAI Validation Layer (This System)
              ↓
Bucket (Memory Layer)
              ↓
InsightFlow (Observability)
              ↓
Sanskar (Analytics Layer)
              ↓
Chayan (Agent Selection)
              ↓
Sūtradhāra (Contract Builder)
              ↓
RAJYA / SAARTHI Systems
```

The NICAI layer acts as a **domain data integrity boundary** for the intelligence pipeline.

---

# Key Features

• domain-level signal validation  
• deterministic trace_id generation (SHA256)  
• strict schema contract enforcement  
• dataset registry verification  
• batch-safe signal processing  
• Bucket artifact emission (memory layer)  
• telemetry emission (observability)  
• Sanskar integration interface  
• FastAPI validation API  

---

# Deterministic Trace ID

The system generates **deterministic trace IDs** to ensure reproducible outputs.

Trace ID generation rule:

```
trace_id = SHA256(signal_id + timestamp + dataset_id)
```

This guarantees:

• same input → same trace_id  
• no randomness  
• full system determinism  

Example:

```
trace_id: 80b8678cd19b352d6f374d972912dca0d5af0fa2ffd4a7f09d68b56d65db23a9
```

---

# Validation Input Contract

The system enforces a strict schema for incoming signals.

### Required Fields

• `signal_id`  
• `timestamp`  
• `latitude`  
• `longitude`  
• `feature_type`  
• `value`  
• `dataset_id`  

Malformed or incomplete signals are **rejected safely**.

---

# Validation Output Contract

Each validated signal produces a deterministic output:

```
{
 "signal_id": "...",
 "status": "ALLOW / FLAG / REJECT",
 "confidence_score": ...,
 "trace_id": "...",
 "reason": "..."
}
```

Rules:

• no additional fields  
• no missing fields  
• strict schema enforcement  

This ensures **downstream compatibility**.

---

# Batch Processing

The validation API supports **batch signal validation**.

### Behavior

• each signal processed independently  
• REJECT signals do not stop batch execution  
• results returned for all signals  
• output order is deterministic (sorted by signal_id)

Example response:

```
{
 "results": [
  { "signal_id": "SIG100", "status": "ALLOW" },
  { "signal_id": "SIG101", "status": "FLAG" },
  { "signal_id": "SIG102", "status": "REJECT" }
 ]
}
```

---

# Bucket Artifact Emission

For each validated signal, the system emits an artifact to the **Bucket memory layer**.

Example artifact:

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

Artifacts are stored in:

```
bucket_artifacts.jsonl
```

Purpose:

• signal traceability  
• lineage tracking  
• memory layer compatibility  

---

# Telemetry & Observability

The system emits telemetry records for **system monitoring and observability**.

Telemetry format:

```
{
 "trace_id": "...",
 "dataset_id": "...",
 "status": "...",
 "confidence_score": ...,
 "timestamp": "..."
}
```

Telemetry records are stored in:

```
telemetry.log
```

Metrics tracked include:

• total signals processed  
• reject rate  
• flag rate  
• dataset mismatch rate  
• confidence score distribution  

---

# Sanskar Integration Interface

The system exposes a **clean interface for the Sanskar intelligence layer**.

Function:

```
get_validated_signals(signals)
```

Rules:

• only ALLOW and FLAG signals returned  
• REJECT signals removed  
• structure remains unchanged  

Example output:

```
[
 { "signal_id": "SIG910", "status": "ALLOW", ... },
 { "signal_id": "SIG911", "status": "FLAG", ... }
]
```

This ensures **plug-and-play integration with Sanskar**.

---

# Project Structure

```
nicai_validation_layer
│
├── main.py
├── validator.py
├── dataset_registry.py
├── schemas.py
├── utils.py
├── bucket_emitter.py
├── telemetry_emitter.py
├── schema.json
├── datasets.json
├── sample_signals.json
├── test_validation.py
├── integration_test.py
├── bucket_artifacts.jsonl
├── telemetry.log
├── REVIEW_PACKET.md
└── README.md
```

---

# How to Run the Project

### 1 Install Dependencies

```
pip install fastapi uvicorn
```

---

### 2 Run Validation Test Script

```
python test_validation.py
```

This script tests:

• valid signals  
• FLAG signals  
• REJECT signals  
• malformed input  
• batch validation  

---

### 3 Run Integration Test (Sanskar Interface)

```
python integration_test.py
```

This test demonstrates:

```
NICAI → Sanskar Integration
ALLOW + FLAG signals forwarded
REJECT signals filtered
```

---

### 4 Start the Validation API

```
uvicorn main:app --reload
```

---

### 5 Open API Documentation

Open in browser:

```
http://127.0.0.1:8000/docs
```

Use Swagger UI to test the `/validate` endpoint.

---

# Example Signal Input

```
{
 "signal_id": "SIG500",
 "timestamp": "2026-03-10T10:00:00Z",
 "latitude": 19.07,
 "longitude": 72.87,
 "feature_type": "weather",
 "value": 34,
 "dataset_id": "DS01"
}
```

---

# Example Validation Output

```
{
 "signal_id": "SIG500",
 "status": "ALLOW",
 "confidence_score": 0.92,
 "trace_id": "80b8678cd19b352d6f374d972912dca0d5af0fa2ffd4a7f09d68b56d65db23a9",
 "reason": "valid signal"
}
```

---

# Failure Handling

The system safely handles:

• missing required fields  
• malformed input signals  
• unregistered datasets  
• inactive datasets  
• emitter failures  

System guarantees:

• validation output always returned  
• batch execution continues  
• system does not crash  

---

# Testing

Testing is performed using:

• `test_validation.py`  
• `integration_test.py`  
• FastAPI `/validate` endpoint  

Test scenarios include:

• valid signals  
• inactive dataset signals  
• missing field signals  
• malformed inputs  
• batch signals  
• Sanskar integration  

All outputs are **deterministic, contract-safe, and batch-consistent**.

---

# Summary

This project implements a **deterministic, observable, and contract-safe domain validation layer for NICAI**.

The system guarantees:

• deterministic validation outputs  
• strict schema contract enforcement  
• traceable validation artifacts  
• telemetry-based observability  
• seamless integration with Sanskar intelligence systems  

The NICAI validation layer ensures that **only trusted, structured, and traceable signals enter the intelligence pipeline**.
