# NICAI End-to-End Validation & Intelligence Pipeline

## Overview

This project implements the **NICAI Domain Data Integrity Layer integrated with a deterministic end-to-end pipeline simulation**.

The system validates incoming signals and passes them through a structured intelligence pipeline while maintaining **strict architectural separation, deterministic behavior, and observability**.

Pipeline Flow:

```
Samachar (Input Signals)
        ↓
NICAI Validation Layer
        ↓
Bucket (Artifact Storage)
        ↓
InsightFlow (Telemetry Logs)
        ↓
Sanskar Analytics Stub
        ↓
Decision Engine Stub
        ↓
Final Pipeline Output
```

The goal of this project is to demonstrate how **validated signals safely propagate through an intelligence pipeline before reaching downstream systems**.

---

# System Responsibilities

The NICAI layer performs the following responsibilities:

- validate incoming signal schema
- verify dataset registry status
- generate deterministic trace identifiers
- emit validation artifacts for memory layer
- emit telemetry metrics for observability
- forward trusted signals to analytics systems
- produce structured pipeline outputs

Architectural principle:

**Validation logic must never contain intelligence or decision logic.**

---

# Key Features

• deterministic signal validation  
• strict schema enforcement  
• SHA256 based `trace_id` generation  
• batch-safe signal processing  
• analytics simulation layer (Sanskar Stub)  
• rule-based decision engine stub  
• structured API pipeline response  
• observability support (Bucket + Telemetry)  
• demo pipeline execution script  

---

# System Architecture

```
Samachar (Input Signals)
        ↓
NICAI Validation Layer
        ↓
Bucket (Artifact Storage)
        ↓
InsightFlow (Telemetry Logs)
        ↓
Sanskar Analytics Stub
        ↓
Decision Engine Stub
        ↓
Pipeline Output
```

NICAI acts as the **gateway ensuring only trusted signals enter the intelligence pipeline.**

---

# Validation Layer

File: `validator.py`

Responsibilities:

- validate required signal fields
- verify dataset registry
- assign validation status
- generate deterministic trace identifiers
- produce structured validation outputs

Validation statuses:

```
ALLOW
FLAG
REJECT
```

Validation Output Format:

```json
{
 "signal_id": "...",
 "status": "...",
 "confidence_score": ...,
 "trace_id": "...",
 "reason": "..."
}
```

---

# Downstream Integration Contract

Validated signals are forwarded to downstream systems using the following contract.

```json
{
 "signal_id": "...",
 "status": "ALLOW | FLAG",
 "confidence_score": ...,
 "trace_id": "...",
 "reason": "..."
}
```

Integration Rules:

• `REJECT` signals are filtered  
• `ALLOW` and `FLAG` signals are forwarded  
• output schema remains deterministic  
• no additional dynamic fields allowed  

This ensures **clean integration with the Sanskar analytics layer.**

---

# Analytics Layer (Sanskar Stub)

File: `sanskar_stub.py`

This module simulates the **analytics layer**.

Behavior:

- accepts validated signals
- computes anomaly score
- assigns signal priority

Analytics Output Format:

```json
{
 "signal_id": "...",
 "status": "...",
 "confidence_score": ...,
 "anomaly_score": ...,
 "priority": "LOW | MEDIUM | HIGH"
}
```

Example rule behavior:

| Anomaly Score | Priority |
|---------------|----------|
| Low           | LOW      |
| Medium        | MEDIUM   |
| High          | HIGH     |

---

# Decision Engine Stub

File: `decision_engine_stub.py`

This module converts analytics results into deterministic decisions.

Decision rules:

```
HIGH anomaly → ALERT
MEDIUM anomaly → REVIEW
LOW anomaly → PROCEED
```

Decision Output Format:

```json
{
 "decision": "...",
 "risk_level": "...",
 "reason": "Decision based on anomaly score"
}
```

---

# API Pipeline Response

The API returns a structured multi-layer response.

```json
{
 "validation": {
   "signal_id": "...",
   "status": "...",
   "confidence_score": ...,
   "trace_id": "...",
   "reason": "..."
 },

 "analytics": {
   "signal_id": "...",
   "status": "...",
   "confidence_score": ...,
   "anomaly_score": ...,
   "priority": "..."
 },

 "decision": {
   "decision": "...",
   "risk_level": "...",
   "reason": "..."
 }
}
```

Special case:

If validation result is **REJECT**, only validation output is returned.

---

# Determinism Guarantee

The system guarantees deterministic behavior.

Measures implemented:

• SHA256 based trace_id generation  
• rule-based analytics scoring  
• rule-based decision engine  
• sorted batch processing  

Result:

```
Same Input
      ↓
Same Validation
      ↓
Same Analytics
      ↓
Same Decision
```

This ensures reproducible and stable system behavior.

---

# Observability

The system supports observability through two mechanisms.

## Bucket (Memory Layer)

Stores validation artifacts.

Storage file:

```
bucket_artifacts.jsonl
```

Artifact Example:

```json
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

Purpose:

- trace continuity
- validation history
- debugging support

---

## Telemetry Logs (InsightFlow)

Telemetry logs capture pipeline metrics.

Storage file:

```
telemetry.log
```

Telemetry Example:

```json
{
 "trace_id": "...",
 "dataset_id": "...",
 "status": "...",
 "confidence_score": ...,
 "timestamp": "..."
}
```

Purpose:

- system monitoring
- validation metrics tracking
- operational visibility

---

# Demo Mode

File: `run_demo.py`

This script simulates signals and runs the full pipeline.

Run command:

```
python run_demo.py
```

Demo Flow:

```
Input Signal
      ↓
Validation Layer
      ↓
Analytics Layer
      ↓
Decision Engine
      ↓
Final Output
```

Example Console Output:

```
INPUT SIGNAL
VALIDATION → ALLOW
ANALYTICS → LOW priority
DECISION → PROCEED
```

This demonstrates the **complete end-to-end pipeline execution.**

---

# Running the Project

## 1 Install Dependencies

```
pip install fastapi uvicorn
```

---

## 2 Run Validation Tests

```
python test_validation.py
```

---

## 3 Run Demo Pipeline

```
python run_demo.py
```

---

## 4 Start API Server

```
uvicorn main:app --reload
```

---

## 5 Open API Documentation

Open in browser:

```
http://127.0.0.1:8000/docs
```

---

# Example API Request

```json
{
 "signal_id": "SIG920",
 "timestamp": "2026-03-10T10:00:00Z",
 "latitude": 19.07,
 "longitude": 72.87,
 "feature_type": "weather",
 "value": 30,
 "dataset_id": "DS01"
}
```

---

# Example API Response

```json
{
 "validation": {
   "signal_id": "SIG920",
   "status": "ALLOW",
   "confidence_score": 0.92,
   "trace_id": "...",
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
```

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
│
├── sanskar_stub.py
├── decision_engine_stub.py
├── run_demo.py
│
├── bucket_emitter.py
├── telemetry_emitter.py
│
├── schema.json
├── datasets.json
├── sample_signals.json
│
├── test_validation.py
├── integration_test.py
│
├── bucket_artifacts.jsonl
├── telemetry.log
│
├── README.md
└── REVIEW_PACKET.md
```

---

# Summary

This project converts the NICAI validation module into a **fully connected deterministic pipeline system**.

The system now provides:

- deterministic signal validation
- analytics simulation layer
- decision simulation layer
- structured pipeline API
- observability support
- demo-ready execution
- downstream integration compatibility

The system is now **integration-ready for intelligence pipelines and downstream systems.**
