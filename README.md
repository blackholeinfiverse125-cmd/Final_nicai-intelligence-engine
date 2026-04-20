# NICAI – Networked Intelligence & Context Analysis Interface

NICAI is a **deterministic intelligence system** that transforms real-world environmental data into structured anomaly insights, pattern detection, and traceable action signals.

It acts as an **intelligence layer between raw data and downstream governance systems**.

---

# 🚀 Overview

NICAI processes datasets such as weather and AQI to:

- Validate incoming signals
- Detect anomalies using rule-based logic
- Identify multi-signal patterns
- Generate structured recommendation signals
- Enable dashboard-based interaction
- Maintain full traceability using `trace_id`

⚠️ NICAI does NOT take decisions  
It ONLY generates **intelligence outputs and recommendation signals**

---

# 🧠 Key Features

- ✅ Deterministic processing (no randomness)
- ✅ Multi-signal pattern detection
- ✅ Full traceability (`trace_id`)
- ✅ Failure-safe system (no crashes)
- ✅ Dashboard visualization
- ✅ Structured logging system
- ✅ TANTRA-aligned outputs
- ✅ Action routing (simulation only)

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
Action Routing (Simulation)
   ↓
Logging System
```

---

# 📂 Project Structure

```
nicai_system/

main.py
validator.py
sanskar_engine.py
samachar_input_adapter.py
dashboard.py
action_router.py
error_handler.py

run_demo_full.py

logs/
data/

REVIEW_PACKET.md
TESTING_PACKET.md
README.md
```

---

# ▶️ How to Run

### Run Full Demo
```
python run_demo_full.py
```

### Run API Manually
```
uvicorn main:app --reload
```

### Open Dashboard
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

Deterministic anomaly detection:

| Condition | Risk |
|----------|------|
| Normal   | LOW  |
| Elevated | MEDIUM |
| Extreme  | HIGH |

### Output Contract

```json
{
  "risk_level": "HIGH",
  "anomaly_type": "TEMPERATURE_SPIKE",
  "explanation": "Extreme temperature detected",
  "confidence": 0.9,
  "temporal_context": "current_window",
  "recommendation_signal": "eligible_for_escalation"
}
```

---

# 📈 Pattern Detection

Handled in `sanskar_engine.py`

Detects:

- repeated anomalies  
- clustered anomalies  
- affected zones  

Example:

```json
{
  "pattern_id": "PATTERN_xxx",
  "anomaly_count": 3,
  "affected_zones": ["North"],
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

---

# 🛡 Failure Handling

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
- safe fallback  
- controlled execution  

---

# 📥 Input Validation Gate

Before processing:

- validates input type  
- checks required fields  
- blocks invalid data  

Invalid input → immediate structured error

---

# 📊 Dashboard

File: `dashboard.py`

Features:

- signal table  
- risk levels  
- anomaly insights  
- action buttons  
- pattern summary  
- trace_id visibility  

Fail-safe mode:

```
No data / invalid input
```

---

# ⚡ API Endpoints

| Endpoint | Method | Description |
|----------|--------|------------|
| `/validate` | POST | Validate signal |
| `/pipeline` | POST | Validation + analysis |
| `/nicai/evaluate` | POST | Final intelligence |
| `/run` | GET | Batch processing |
| `/dashboard` | GET | UI dashboard |
| `/action` | POST | Action logging |

---

# 📊 Logging System

Logs stored in:

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

# 🔒 Deterministic Guarantee

```
Same Input → Same Output
```

---

# 📌 Final Status

- ✅ Integrated  
- ✅ Crash-free  
- ✅ Failure-safe  
- ✅ Deterministic  
- ✅ Traceable  
- ✅ Demo-ready  
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
- generates structured recommendation signals  
- ensures full traceability  

Ready for **demo and controlled deployment**.
