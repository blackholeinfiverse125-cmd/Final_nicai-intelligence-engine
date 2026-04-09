# NICAI End-to-End Validation & Intelligence Pipeline

## Overview

This project implements the **NICAI Domain Data Integrity Layer integrated with an end-to-end pipeline simulation**.

The system validates incoming signals and passes them through a deterministic pipeline that simulates downstream intelligence layers.

Pipeline Flow:

```
Samachar (Input Signals)
        ↓
NICAI Validation Layer
        ↓
Sanskar Analytics Stub
        ↓
Decision Engine Stub
        ↓
Final Structured Output
```

The goal of this project is to demonstrate how **validated signals flow through an intelligence pipeline while maintaining deterministic behavior, observability, and strict architectural separation.**

---

# System Responsibilities

The NICAI layer performs the following responsibilities:

- validates incoming signal schema
- verifies dataset registry status
- generates deterministic trace identifiers
- emits validation artifacts to Bucket
- emits telemetry logs for observability
- forwards valid signals to analytics layer
- produces structured multi-layer outputs

Important architectural rule:

**Validation logic is never mixed with intelligence or decision logic.**

---

# Key Features

• deterministic signal validation  
• strict schema enforcement  
• SHA256 based trace_id generation  
• batch-safe signal processing  
• analytics simulation layer (Sanskar Stub)  
• rule-based decision simulation layer  
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
- generate deterministic trace_id
- produce structured validation output

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

# Analytics Layer (Sanskar Stub)

File: `sanskar_stub.py`

This module simulates the **analytics layer**.

Behavior:

- accepts validated signals
- calculates anomaly score
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

This layer prepares signals for decision processing.

---

# Decision Engine Stub

File: `decision_engine_stub.py`

This module simulates the decision layer.

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

The system guarantees deterministic outputs.

Measures implemented:

- SHA256 based trace_id generation
- rule-based analytics scoring
- rule-based decision engine
- sorted batch processing

Result:

```
Same Input → Same Validation → Same Analytics → Same Decision
```

---

# Observability

The system supports observability through two mechanisms.

## Bucket (Memory Layer)

Stores validation artifacts.

Example storage file:

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

---

## Telemetry Logs (InsightFlow)

Telemetry logs capture pipeline metrics.

Example storage file:

```
telemetry.log
```

Telemetry Record Example:

```json
{
 "trace_id": "...",
 "dataset_id": "...",
 "status": "...",
 "confidence_score": ...,
 "timestamp": "..."
}
```

---

# Demo Mode

File: `run_demo.py`

This script simulates signals and executes the full pipeline.

Command:

```bash
python run_demo.py
```

Example Console Output:

```
INPUT SIGNAL

VALIDATION RESULT
ALLOW

ANALYTICS RESULT
LOW priority signal

DECISION
PROCEED
```

This demonstrates the **complete pipeline execution**.

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

This project converts the NICAI validation module into a **fully connected deterministic pipeline demonstration system**.

The system now provides:

- deterministic signal validation
- analytics simulation layer
- decision simulation layer
- structured pipeline API
- observability support
- demo-ready execution

The system is now **integration-ready for downstream intelligence systems.**
