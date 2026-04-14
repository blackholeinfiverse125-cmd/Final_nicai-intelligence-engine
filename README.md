# NICAI – Networked Intelligence & Context Analysis Interface

A deterministic intelligence system that processes real-world datasets, detects anomalies, and provides actionable intelligence through a dashboard without executing decisions.

NICAI transforms raw signals into structured intelligence while maintaining **traceability, transparency, and deterministic outputs**.

---

# System Overview

NICAI acts as an **intelligence layer** between raw data sources and governance systems.

It performs:

* Signal validation
* Deterministic anomaly detection
* Risk analysis
* Multi-signal intelligence
* Dashboard visualization
* Structured action routing

Important:
NICAI **does not execute decisions**.
It only produces intelligence outputs and action payloads.

---

# System Architecture

```
Dataset
   ↓
Samachar Input Adapter
   ↓
Signal Conversion
   ↓
Validation Layer
   ↓
Intelligence Engine
   ↓
Multi-Signal Analyzer
   ↓
Dashboard Interface
   ↓
User Action Trigger
   ↓
Action Payload Generation
   ↓
Action Logs
```

---

# Key Features

## Deterministic Validation Layer

Ensures signal integrity and traceability.

Outputs:

* status
* confidence score
* trace ID

---

## Intelligence Engine

Detects anomalies and generates structured explanations.

Produces:

* anomaly score
* risk level
* anomaly type
* explanation
* recommendation signal

---

## Multi-Signal Intelligence

Analyzes signal clusters to detect patterns across datasets.

Outputs:

* anomaly count
* affected zones
* pattern summary

---

## FastAPI Dashboard

Displays real-time intelligence information including:

* Signal ID
* Validation Status
* Risk Level
* Anomaly Type
* Explanation
* Recommendation Signal

---

## Action Interface

Users can trigger actions from the dashboard.

Available actions:

* Escalate
* Review
* Assign

NICAI generates structured action payloads instead of executing actions.

Example payload:

```json
{
 "trace_id": "acf999a9afdfaabee481b750fc75e0ffa1648ba14cb38b9187776d30e85a3bf9",
 "action_type": "ESCALATE",
 "target_role": "authority",
 "timestamp": "2026-04-14T04:21:32"
}
```

Actions are logged into:

```
action_logs.json
```

---

# Dataset Sources

NICAI currently ingests multiple real datasets.

Examples:

Weather Dataset
Used for temperature anomaly detection.

AQI Dataset
Used for pollution anomaly detection.

Datasets are processed using:

```
samachar_input_adapter.py
```

---

# Project Structure

```
nicai_validation_layer
│
├── data
│   ├── clean_aqi.csv
│   ├── clean_weather.csv
│
├── validator.py
├── analytics_engine.py
├── multi_signal_analyzer.py
├── samachar_input_adapter.py
│
├── dashboard.py
├── run_demo_full.py
│
├── action_logs.json
├── telemetry_metrics.json
│
├── REVIEW_PACKET.md
├── TESTING_PACKET.md
│
└── README.md
```

---

# Installation

Clone repository:

```
git clone https://github.com/your-repository/nicai-system.git
```

Navigate to project directory:

```
cd nicai_validation_layer
```

Install dependencies:

```
pip install fastapi uvicorn pandas
```

---

# Running the System

## Run Full NICAI Demo

```
python run_demo_full.py
```

This performs:

1. Dataset ingestion
2. Signal generation
3. Validation
4. Intelligence analysis
5. Multi-signal pattern detection
6. Dashboard instructions

---

# Launch Dashboard

Run:

```
uvicorn dashboard:app --reload
```

Open browser:

```
http://127.0.0.1:8000
```

The dashboard will display:

* signals
* anomaly types
* risk levels
* explanations

---

# Action Logging

When dashboard actions are triggered, the system logs payloads in:

```
action_logs.json
```

Example:

```
{
 "trace_id": "...",
 "action_type": "ESCALATE",
 "target_role": "authority",
 "timestamp": "2026-04-14T04:21:32"
}
```

---

# Observability

System telemetry is stored in:

```
telemetry_metrics.json
```

Logs include:

* validation events
* anomaly detection
* system execution stages
* action routing

---

# Demo Execution Flow

1 Run demo script

```
python run_demo_full.py
```

2 Start dashboard

```
uvicorn dashboard:app --reload
```

3 Open browser

```
http://127.0.0.1:8000
```

4 Trigger actions from dashboard

5 Verify logs

```
action_logs.json
```

---

# Testing

Testing instructions are provided in:

```
TESTING_PACKET.md
```

Testing includes:

* input validation
* anomaly detection
* dashboard actions
* log verification
* failure scenarios

---

# System Status

The system currently supports:

* real dataset ingestion
* deterministic signal validation
* anomaly detection
* multi-signal intelligence
* dashboard visualization
* action payload routing
* telemetry logging

The system is **demo-ready and locally executable**.

---

# Developer

**Ankita Prajapati**

Role:
NICAI Core Developer

Responsibilities:

* Validation Layer
* Intelligence Engine
* Dashboard API
* Action Routing
* Demo Integration

---
