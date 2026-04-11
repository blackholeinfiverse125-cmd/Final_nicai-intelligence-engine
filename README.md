# NICAI – TANTRA Integration Ready Pipeline

## Overview

This project implements the **NICAI Domain Data Integrity and Intelligence Pipeline** prepared for integration into the **TANTRA system architecture**.

The system receives structured signals, validates them, performs deterministic analytics, generates decisions, and exposes a **clean API interface for external systems**.

NICAI operates as a **self-contained, deployable domain system** designed to integrate seamlessly with the following TANTRA components:

* **Samachar** → upstream signal provider
* **Mitra** → interface layer consuming NICAI outputs
* **Simulation systems (Rudra / Atharva)** → downstream consumers
* **Testing framework (Vinayak Tiwari)** → system verification

The architecture ensures **clean system boundaries, deterministic outputs, and safe pipeline execution**.

---

# System Architecture

The NICAI system processes signals through a structured pipeline.

```
Samachar (Signal Input)
        ↓
Input Adapter
        ↓
NICAI Validation Layer
        ↓
Analytics Engine
        ↓
Decision Engine
        ↓
NICAI Output API
        ↓
Mitra / Simulation / Downstream Systems
```

The pipeline ensures that **only validated signals propagate through the intelligence layers**.

---

# System Responsibilities

NICAI performs the following responsibilities:

• validate incoming signals
• verify dataset registry
• generate deterministic trace identifiers
• compute deterministic anomaly scores
• produce risk-based decisions
• expose decision-ready API outputs
• maintain clean integration boundaries

Architectural rule:

**Validation logic must remain independent from analytics and decision logic.**

---

# Final Output Contract (TANTRA Integration)

The NICAI system produces a **canonical output contract** used by downstream systems.

```
{
  signal_id,
  status,
  confidence_score,
  trace_id,
  reason,
  anomaly_score,
  priority,
  decision,
  risk_level,
  summary_line,
  explanation
}
```

This structure ensures compatibility with **Mitra interface systems and simulation environments**.

---

# Input Format (Samachar Compatibility)

NICAI accepts structured signals compatible with **Samachar input format**.

Example Input:

```json
{
 "signal_id": "SIG300",
 "value": 95,
 "dataset_id": "DS01"
}
```

The **Samachar Input Adapter** normalizes incoming signals before validation.

File:

```
samachar_input_adapter.py
```

Responsibilities:

• normalize input schema
• enforce required fields
• prepare signals for validation

---

# Validation Layer

File:

```
validator.py
```

The validation layer verifies signal integrity before allowing pipeline processing.

Responsibilities:

• verify required fields
• validate dataset registry
• generate deterministic trace identifiers
• assign validation status

Validation statuses:

```
ALLOW
FLAG
REJECT
```

Validation Output Example:

```json
{
 "signal_id": "SIG300",
 "status": "ALLOW",
 "confidence_score": 0.92,
 "trace_id": "...",
 "reason": "valid signal"
}
```

Pipeline behavior:

| Status | Behavior          |
| ------ | ----------------- |
| ALLOW  | continue pipeline |
| FLAG   | continue pipeline |
| REJECT | stop pipeline     |

---

# Analytics Engine

File:

```
analytics_engine.py
```

The analytics engine evaluates signal anomaly levels using **deterministic rules**.

No machine learning or randomness is used.

Example scoring rules:

| Signal Value | Anomaly Score | Priority |
| ------------ | ------------- | -------- |
| < 70         | 0.08          | LOW      |
| 70 – 89      | 0.55          | MEDIUM   |
| ≥ 90         | 0.90          | HIGH     |

Analytics Output Example:

```json
{
 "anomaly_score": 0.9,
 "priority": "HIGH"
}
```

---

# Decision Engine

File:

```
decision_engine.py
```

The decision engine converts analytics results into system actions.

Decision rules:

```
HIGH priority → ALERT
MEDIUM priority → REVIEW
LOW priority → PROCEED
```

Decision Output Example:

```json
{
 "decision": "ALERT",
 "risk_level": "HIGH",
 "reason": "Decision based on anomaly score"
}
```

---

# NICAI API Interface

The system exposes a **decision-ready API** designed for Mitra integration.

Endpoint:

```
POST /nicai/evaluate
```

Example Request:

```json
{
 "signal_id": "SIG300",
 "value": 95,
 "dataset_id": "DS01"
}
```

Example Response:

```json
{
 "signal_id": "SIG300",
 "status": "ALLOW",
 "confidence_score": 0.92,
 "trace_id": "...",
 "reason": "valid signal",
 "anomaly_score": 0.9,
 "priority": "HIGH",
 "decision": "ALERT",
 "risk_level": "HIGH",
 "summary_line": "Signal ALERT with HIGH priority",
 "explanation": "Decision based on anomaly score"
}
```

The output is **human-readable and decision-ready** for external systems.

---

# Error Handling

File:

```
error_handler.py
```

The system includes safe error handling mechanisms.

Behavior:

• prevents system crashes
• returns structured error responses
• preserves pipeline stability

Example Error Output:

```json
{
 "error": "invalid signal format"
}
```

---

# Deterministic Behavior

The NICAI system guarantees deterministic outputs.

Measures implemented:

• SHA256 based trace_id generation
• rule-based analytics scoring
• rule-based decision engine
• no randomness

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

This ensures reproducible system behavior.

---

# Running the System

## Install Dependencies

```
pip install fastapi uvicorn
```

---

## Start API Server

```
uvicorn main:app --reload
```

---

## Open API Documentation

```
http://127.0.0.1:8000/docs
```

Use the endpoint:

```
POST /nicai/evaluate
```

---

# Project Structure

```
nicai_validation_layer
│
├── main.py
├── validator.py
├── analytics_engine.py
├── decision_engine.py
│
├── samachar_input_adapter.py
├── error_handler.py
│
├── dataset_registry.py
├── schemas.py
├── utils.py
│
├── sample_signals.json
├── datasets.json
│
├── run_demo.py
├── test_validation.py
│
├── README.md
├── REVIEW_PACKET.md
└── TESTING_PACKET.md
```

---

# Testing

Testing instructions are documented in:

```
TESTING_PACKET.md
```

The testing packet includes:

• API endpoints
• sample inputs
• expected outputs
• failure cases
• deterministic verification

---

# Demo Flow

The demo demonstrates the following steps:

1. Input signal submission
2. Validation layer processing
3. Analytics anomaly evaluation
4. Decision generation
5. Final structured output

The demonstration confirms that **NICAI produces deterministic intelligence decisions from validated signals**.

---

# Summary

This project implements a **fully deployable NICAI intelligence pipeline prepared for integration with the TANTRA ecosystem**.

The system provides:

• deterministic signal validation
• analytics-based anomaly detection
• rule-based decision generation
• clean API interface for Mitra
• safe error handling
• deterministic pipeline behavior

NICAI now functions as a **standalone domain system ready to plug into the TANTRA architecture**.
