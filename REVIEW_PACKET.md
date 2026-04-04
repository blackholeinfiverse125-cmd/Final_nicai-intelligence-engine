# NICAI Domain Data Integrity Layer – Review Packet

---

# 1. ENTRY POINT

**File:** `main.py`

This file acts as the entry point for the validation system and exposes the API endpoint:

```
POST /validate
```

The endpoint receives raw signals from the **Samachar layer** and sends them to the validation logic.

The API supports:

* Single signal validation
* Batch signal validation

The validation layer **only processes signals and returns validation results**.

It does **not**:

* enforce decisions
* control pipeline execution

---

# 2. CORE FLOW (MAX 3 FILES)

## main.py

Handles the API interface for the validation system.

Responsibilities:

* receives incoming signals
* determines single or batch input
* sends signals to the validation layer
* returns structured validation responses

---

## validator.py

Contains the core validation logic.

Responsibilities:

* validate signal schema
* check required fields
* verify dataset registry
* assign validation status (`ALLOW / FLAG / REJECT`)
* generate trace identifiers
* support batch-safe processing

Each signal is processed **independently**.

---

## dataset_registry.py

Provides access to dataset metadata stored in the dataset registry.

Responsibilities:

* dataset lookup
* dataset status verification
* dataset trust score retrieval

Dataset metadata is stored in:

```
datasets.json
```

---

# 3. LIVE FLOW (REAL INPUT → OUTPUT)

## Example Input Signal (Samachar)

```json
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

## Processing Flow

```
Samachar (Raw Structured Input)
        ↓
Validation Layer
        ↓
Schema Validation
        ↓
Dataset Registry Check
        ↓
Validation Result Generated
```

---

## Example Output

```json
{
 "signal_id": "SIG500",
 "status": "ALLOW",
 "confidence_score": 0.92,
 "trace_id": "generated_uuid",
 "reason": "valid signal"
}
```

The validation layer produces structured validation results **without stopping pipeline execution**.

---

# 4. WHAT WAS BUILT

A **domain-level data integrity validation layer** for NICAI that prepares signals for downstream analytics systems.

### Implemented Capabilities

* schema validation for incoming signals
* dataset registry verification
* validation status classification (`ALLOW / FLAG / REJECT`)
* trace identifier generation using UUID
* batch-safe processing of signals
* deterministic validation outputs for analytics systems

The validation layer strictly separates:

* **validation logic**
* **decision logic**

---

## System Guarantees

The system does **not**:

* enforce governance rules
* stop pipeline execution
* make decisions for downstream systems

It ensures that signals passed to analytics systems are **clean, structured, and trusted**.

---

# 5. FAILURE CASES HANDLED

The validation layer safely handles multiple failure scenarios.

### Handled Cases

* missing required fields
* malformed input signals
* invalid schema structure
* unregistered datasets
* inactive datasets

---

## Failure Behavior

* system does **not crash**
* batch processing continues
* structured **REJECT responses** are returned

### Example Failure Output

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

# 6. PROOF

Validation testing was performed using **two methods**.

---

## Script Testing

Testing file:

```
test_validation.py
```

Command used:

```
python test_validation.py
```

### Test Scenarios

* valid signal validation
* inactive dataset validation
* missing field validation
* mixed batch validation
* malformed input validation

All outputs were **deterministic and consistent**.

---

## API Testing

The validation API was tested using **FastAPI Swagger UI**.

Endpoint tested:

```
POST /validate
```

### Test Scenarios

* Single signal → `ALLOW`
* Inactive dataset signal → `FLAG`
* Missing field signal → `REJECT`
* Batch signals → mixed validation results

All signals were processed **independently without stopping batch execution**.

---

# 7. HOW TO RUN THE SYSTEM

## Step 1 — Install Dependencies

```
pip install fastapi uvicorn
```

---

## Step 2 — Run Validation Test Script

```
python test_validation.py
```

This script executes multiple validation scenarios and prints validation outputs.

---

## Step 3 — Start the Validation API Server

```
uvicorn main:app --reload
```

---

## Step 4 — Open API Documentation

Open in browser:

```
http://127.0.0.1:8000/docs
```

---

## Step 5 — Test the Validation Endpoint

Use the **POST /validate** endpoint.

### Example Single Signal Input

```json
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

### Example Batch Input

```json
[
 {
  "signal_id": "SIG500",
  "timestamp": "2026-03-10T10:00:00Z",
  "latitude": 19.07,
  "longitude": 72.87,
  "feature_type": "weather",
  "value": 34,
  "dataset_id": "DS01"
 },
 {
  "signal_id": "SIG501",
  "timestamp": "2026-03-10T10:05:00Z",
  "latitude": 18.52,
  "longitude": 73.85,
  "feature_type": "vessel",
  "value": 120,
  "dataset_id": "DS02"
 }
]
```

---

# SYSTEM ARCHITECTURE POSITION

```
Samachar (Raw Structured Signals)
        ↓
Validation Layer (This Implementation)
        ↓
Sanskar (Analytics Layer)
        ↓
Mitra (Decision Layer)
        ↓
UI and Simulation Systems
```

The validation layer acts as a **domain boundary** that prepares trusted signals for analytics systems.

---

# SUMMARY

This implementation converts the signal validation component into a **domain-level data integrity layer aligned with the NICAI architecture**.

The system guarantees:

* schema-safe validation
* batch-safe signal processing
* deterministic validation results
* trusted signals for analytics systems
* clear separation between validation and decision logic
