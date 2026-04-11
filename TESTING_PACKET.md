# TESTING_PACKET.md

# NICAI Pipeline Testing Packet

This document provides the complete testing guide for verifying the **NICAI deterministic pipeline**.
It allows testers to validate the full system behavior including **validation, analytics, decision generation, and failure handling**.

---

# 1. System Overview

The NICAI pipeline processes structured signals and produces deterministic decisions.

Pipeline Flow:

```
Signal Input
     ↓
Validation Layer
     ↓
Analytics Engine
     ↓
Decision Engine
     ↓
Final Decision Output
```

The system guarantees:

* Deterministic outputs (same input → same output)
* Clean API contract
* Failure-safe processing
* Clear decision explanations

---

# 2. API Endpoints

The system exposes the following API endpoints.

### 1. Validation API

```
POST /validate
```

Purpose:
Validates signal structure and dataset registry.

Output:
Validation result only.

---

### 2. Pipeline API

```
POST /pipeline
```

Purpose:
Runs validation + analytics + decision pipeline.

Output:
Multi-layer response.

---

### 3. Final NICAI Evaluation API

```
POST /nicai/evaluate
```

Purpose:
Produces the **final decision-ready output** used by the Mitra interface.

This endpoint is the **primary interface for system integration**.

---

# 3. How to Run the System

Start the API server using the command:

```
uvicorn main:app --reload
```

Open API documentation in browser:

```
http://127.0.0.1:8000/docs
```

From the Swagger interface, select:

```
POST /nicai/evaluate
```

Run the test cases listed below.

---

# 4. Test Cases

The following test cases verify the complete system behavior.

---

# Test Case 1 — LOW Anomaly Signal

Input:

```json
{
 "signal_id": "SIG100",
 "value": 30,
 "dataset_id": "DS01"
}
```

Expected Output:

```
status: ALLOW
priority: LOW
decision: PROCEED
risk_level: LOW
```

Explanation:

Signal value is within normal range.
System allows the signal and proceeds without risk.

---

# Test Case 2 — MEDIUM Anomaly Signal

Input:

```json
{
 "signal_id": "SIG200",
 "value": 75,
 "dataset_id": "DS01"
}
```

Expected Output:

```
status: ALLOW
priority: MEDIUM
decision: REVIEW
risk_level: MEDIUM
```

Explanation:

Signal shows moderate anomaly.
System flags the signal for review.

---

# Test Case 3 — HIGH Anomaly Signal

Input:

```json
{
 "signal_id": "SIG300",
 "value": 95,
 "dataset_id": "DS01"
}
```

Expected Output:

```
status: ALLOW
priority: HIGH
decision: ALERT
risk_level: HIGH
```

Explanation:

Signal value exceeds safe threshold.
System generates a high-priority alert.

---

# Test Case 4 — Dataset Not Registered

Input:

```json
{
 "signal_id": "SIG400",
 "value": 50,
 "dataset_id": "UNKNOWN"
}
```

Expected Output:

```
status: REJECT
reason: dataset not registered
```

Explanation:

Dataset does not exist in the registry.
Validation rejects the signal.

---

# Test Case 5 — Inactive Dataset

Input:

```json
{
 "signal_id": "SIG500",
 "value": 60,
 "dataset_id": "DS02"
}
```

Expected Output:

```
status: FLAG
priority: MEDIUM
decision: REVIEW
risk_level: MEDIUM
```

Explanation:

Dataset exists but is marked inactive.
Signal is flagged but still processed by downstream layers.

---

# 5. Determinism Verification

To verify deterministic behavior:

Run the same input multiple times.

Example input:

```json
{
 "signal_id": "SIG300",
 "value": 95,
 "dataset_id": "DS01"
}
```

Expected behavior:

```
Same input → Same output every time
```

This confirms that the pipeline contains **no randomness**.

---

# 6. Failure Handling Verification

The system must handle failures safely.

Scenarios tested:

Missing fields
Invalid dataset
Inactive dataset

Expected behavior:

```
System does not crash
Proper error or validation response returned
```

---

# 7. Expected System Guarantees

The NICAI pipeline guarantees the following properties:

* Deterministic signal evaluation
* Strict validation before analytics
* Clean separation of validation, analytics, and decision layers
* Human-readable decision output
* Production-safe error handling

---

# 8. Testing Outcome

If all test cases pass successfully, the system confirms:

* Validation layer correctness
* Analytics engine behavior
* Decision engine logic
* API contract stability
* Deterministic pipeline execution

The NICAI pipeline is then considered **ready for integration into the TANTRA architecture**.

---
