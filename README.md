# NICAI Signal Evaluation Pipeline (TANTRA Integration)

## Overview

This project implements the **NICAI signal evaluation system**, which acts as a validation and intelligence pipeline within the **TANTRA architecture**.

The system receives structured signals, validates them, performs analytics, and generates deterministic decision outputs.
It is designed to simulate integration with other TANTRA components while maintaining **clean architectural boundaries and deterministic behavior**.

The pipeline ensures that only valid and trusted signals are processed by downstream systems.

---

## System Architecture

The system follows a layered pipeline architecture:

```
Samachar (Input Signals)
        ↓
NICAI Validation Layer
        ↓
Analytics Engine
        ↓
Decision Engine
        ↓
Final Decision Output
```

Each layer performs a specific responsibility while keeping the system modular and extensible.

---

## Key Features

* deterministic signal validation
* structured analytics processing
* rule-based decision engine
* clean API integration layer
* simulation-ready architecture
* compatibility with future TANTRA components

---

## Final Output Contract

The NICAI system produces the following structured output:

```json
{
  "signal_id": "...",
  "status": "...",
  "confidence_score": 0.0,
  "trace_id": "...",
  "reason": "...",
  "anomaly_score": 0.0,
  "priority": "...",
  "decision": "...",
  "risk_level": "...",
  "summary_line": "...",
  "explanation": "..."
}
```

This output format is designed for integration with downstream systems such as **Mitra** and future simulation systems.

---

## API Endpoints

The system exposes three REST APIs.

### 1. Validation API

```
POST /validate
```

Performs signal validation only.

Example input:

```json
{
 "signal_id": "SIG100",
 "value": 80,
 "dataset_id": "DS01"
}
```

---

### 2. Pipeline API

```
POST /pipeline
```

Runs the full NICAI pipeline including validation, analytics, and decision stages.

Output includes structured responses from all pipeline layers.

---

### 3. NICAI Evaluation API

```
POST /nicai/evaluate
```

This endpoint provides the **final decision-ready output** for the TANTRA system.

Example response:

```json
{
 "signal_id": "SIG100",
 "status": "ALLOW",
 "confidence_score": 0.92,
 "trace_id": "...",
 "reason": "valid signal",
 "anomaly_score": 0.08,
 "priority": "LOW",
 "decision": "PROCEED",
 "risk_level": "LOW",
 "summary_line": "Signal PROCEED with LOW priority",
 "explanation": "Decision based on anomaly score"
}
```

---

## Validation Rules

The validation layer performs the following checks:

* required signal fields
* dataset registry verification
* dataset status validation
* deterministic trace_id generation

Possible validation statuses:

```
ALLOW
FLAG
REJECT
```

Rules:

* **ALLOW** → signal moves to analytics
* **FLAG** → pipeline continues but marked as medium risk
* **REJECT** → pipeline stops at validation

---

## Analytics Engine

The analytics engine computes the **anomaly score** and assigns signal priority.

Priority levels:

```
LOW
MEDIUM
HIGH
```

This stage simulates the analytics capability of future TANTRA systems.

---

## Decision Engine

The decision engine converts analytics output into deterministic decisions.

Decision rules:

```
HIGH anomaly → ALERT
MEDIUM anomaly → REVIEW
LOW anomaly → PROCEED
```

This provides a final decision that can be consumed by downstream systems.

---

## Deterministic Design

The system is fully deterministic.

This means:

```
Same Input
   ↓
Same Validation
   ↓
Same Analytics
   ↓
Same Decision
```

Deterministic behavior ensures reliable integration with other components.

---

## Running the Project

### Install Dependencies

```
pip install fastapi uvicorn
```

### Start the API Server

```
uvicorn main:app --reload
```

### Open API Documentation

```
http://127.0.0.1:8000/docs
```

This opens the interactive Swagger API interface.

---

## Project Structure

```
nicai_validation_layer
│
├── main.py
├── validator.py
├── analytics_engine.py
├── decision_engine.py
├── samachar_input_adapter.py
├── error_handler.py
│
├── dataset_registry.py
├── datasets.json
│
├── utils.py
├── schemas.py
├── schema.json
│
├── bucket_emitter.py
├── telemetry_emitter.py
│
├── sample_signals.json
│
├── README.md
├── REVIEW_PACKET.md
├── TESTING_PACKET.md
```

---

## Demo Flow

The demo demonstrates the following steps:

1. Input signal submission
2. Validation of the signal
3. Analytics computation
4. Decision generation
5. Final structured response

This demonstrates how NICAI functions as a **signal evaluation component inside the TANTRA ecosystem**.

---

## Conclusion

This project converts the NICAI validation module into a **complete signal evaluation pipeline** that supports deterministic analytics and decision outputs.

The system is now ready to integrate with other TANTRA components and demonstrates a clean architecture suitable for scalable intelligence pipelines.
