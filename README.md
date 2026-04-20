# NICAI – Networked Intelligence & Context Analysis Interface

NICAI is a **deterministic intelligence system** that transforms real-world environmental data into structured anomaly insights, pattern detection, and traceable action signals.

It acts as an **intelligence layer between raw data and governance systems**.

---

# 🚀 Overview

NICAI processes datasets such as weather and AQI to:

- Validate incoming signals
- Detect anomalies using rule-based logic
- Identify multi-signal patterns
- Provide structured recommendations
- Enable dashboard-based interaction
- Maintain full traceability using `trace_id`

⚠️ NICAI does NOT take decisions  
It only generates **intelligence outputs and action recommendations**

---

# 🧠 Key Features

- ✅ Deterministic processing (no randomness)
- ✅ Multi-signal pattern detection
- ✅ Full traceability (`trace_id`)
- ✅ Fail-safe system (no crashes)
- ✅ Dashboard visualization
- ✅ Structured logging system
- ✅ TANTRA-aligned outputs

---

# 🏗 System Architecture

```
Dataset
   ↓
Samachar Input Adapter
   ↓
Signal Conversion
   ↓
Input Validation Gate
   ↓
Validation Layer
   ↓
Sanskar Intelligence Engine
   ↓
Pattern Detection
   ↓
FastAPI Layer
   ↓
Dashboard Interface
   ↓
Action Logging
```

---

# 📂 Project Structure

```
nicai_system/

main.py                  # API layer
validator.py             # validation logic
sanskar_engine.py        # anomaly + pattern detection
samachar_input_adapter.py
dashboard.py             # UI dashboard
error_handler.py         # failure-safe handling

run_demo_full.py         # single entry demo

logs/
data/

REVIEW_PACKET.md
TESTING_PACKET.md
README.md
```

---

# ▶️ How to Run (Single Command Demo)

Run full system:

```
python run_demo_full.py
```

Start API:

```
uvicorn main:app --reload
```

Open dashboard:

```
http://127.0.0.1:8000/dashboard
```

---

# 📊 NICAI Signal Format

```json
{
  "signal_id": "W_2",
  "timestamp": "2026-04-14T04:21:32",
  "latitude": 19.07,
  "longitude": 72.87,
  "value": 48.7,
  "dataset_id": "weather",
  "feature_type": "temperature"
}
```

---

# 🔍 Validation Layer

File: `validator.py`

Responsibilities:

- schema validation
- missing field detection
- dataset verification
- trace_id generation

Output:

```json
{
  "signal_id": "...",
  "status": "VALID | FLAG | ERROR",
  "confidence_score": 0.9,
  "trace_id": "...",
  "reason": "..."
}
```

---

# ⚙️ Intelligence Engine

File: `sanskar_engine.py`

Performs deterministic anomaly detection:

| Condition | Risk |
|----------|------|
| Normal   | LOW  |
| Elevated | MEDIUM |
| Extreme  | HIGH |

Output:

```json
{
  "risk_level": "HIGH",
  "anomaly_score": 0.9,
  "anomaly_type": "TEMPERATURE_SPIKE",
  "explanation": "Extreme temperature detected",
  "recommendation_signal": "eligible_for_escalation"
}
```

---

# 📈 Pattern Detection

Also handled in `sanskar_engine.py`

Detects:

- repeated anomalies
- clustered anomalies
- affected zones

Example:

```json
{
  "pattern_id": "PATTERN_xxx",
  "anomaly_count": 3,
  "affected_zones": ["Zone_A"],
  "pattern_type": "REPEATED_ANOMALY",
  "severity_trend": "STABLE"
}
```

---

# 🧭 TANTRA Compliance

NICAI does NOT take decisions.

Allowed outputs:

- `eligible_for_escalation`
- `requires_review`
- `monitor`

❌ Removed:
- ESCALATE  
- REVIEW  

---

# 🛡 Failure Handling (Critical)

Handled via `error_handler.py`

All errors return:

```json
{
  "status": "ERROR",
  "reason": "clear message",
  "trace_id": "optional"
}
```

System guarantees:

- no crashes  
- no undefined behavior  
- safe execution  

---

# 📥 Input Validation Gate

Before processing:

- checks input format
- ensures required fields
- blocks invalid data early

Invalid input → immediate structured error

---

# 📊 Dashboard

File: `dashboard.py`

Features:

- signal table
- anomaly insights
- action buttons
- pattern summary

Fail-safe mode:

```
No data / invalid input
```

---

# ⚡ API Endpoints

| Endpoint | Method | Description |
|----------|--------|------------|
| `/validate` | POST | Validate signal |
| `/pipeline` | POST | Run validation + analysis |
| `/nicai/evaluate` | POST | Final intelligence output |
| `/run` | GET | Batch processing |
| `/dashboard` | GET | UI dashboard |
| `/action` | POST | Log action |

---

# 📊 Logging System

All logs stored in:

```
logs/
```

Files:

- validation_logs.json  
- anomaly_logs.json  
- pattern_logs.json  
- action_logs.json  

Log format:

```json
{
  "trace_id": "...",
  "timestamp": "...",
  "type": "VALIDATION | ANALYSIS | PATTERN | ACTION",
  "data": {}
}
```

---

# 🔗 Traceability

Each signal gets a `trace_id`.

Flow:

```
Signal → Validation → Analysis → Pattern → Dashboard → Action Log
```

---

# 🎯 Demo Flow (2–3 Minutes)

1. Show dataset  
2. Convert to signals  
3. Run validation  
4. Show anomaly detection  
5. Show pattern detection  
6. Open dashboard  
7. Trigger action  
8. Show logs + trace_id  

---

# 🔒 Deterministic Guarantee

```
Same Input → Same Output
```

- rule-based logic  
- fixed thresholds  
- SHA-based trace_id  

---

# 📌 Final Status

- ✅ Fully integrated system  
- ✅ Crash-free  
- ✅ Demo-ready  
- ✅ Failure-safe  
- ✅ Deterministic  
- ✅ TANTRA-aligned  

---

# 👩‍💻 Developer

**Ankita Prajapati**  
NICAI – System Integration & Stabilization

---

# 📌 Conclusion

NICAI is a **stable, deterministic intelligence system** that:

- processes real-world data  
- detects anomalies  
- identifies patterns  
- provides structured recommendations  
- ensures full traceability  

It is now **demo-ready and production-grade (controlled environments)**.
