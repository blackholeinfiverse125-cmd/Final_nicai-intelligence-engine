# NICAI TESTING PACKET

Project: NICAI Intelligence System  
Developer: Ankita Prajapati  
Testing Authority: Vinayak Tiwari  
Testing Protocol: BHIV Universal Testing Protocol  

---

# 1. SYSTEM OVERVIEW

NICAI is a deterministic intelligence system designed to process real-world datasets and produce structured anomaly intelligence outputs.

The system does NOT execute decisions.

Instead, it performs intelligence analysis and routes action triggers through a dashboard interface.

Pipeline:

Data Ingestion → Signal Conversion → Validation → Intelligence Analysis → Multi-Signal Pattern Detection → Dashboard Visualization → Action Trigger → Logging

---

# 2. REAL DATA INGESTION

NICAI uses real-world datasets for simulation.

Datasets used:

clean_weather.csv  
clean_aqi.csv  

Weather Dataset Source:

OpenWeather / Kaggle climate datasets.

Contains:

timestamp  
temperature  
latitude  
longitude  

AQI Dataset Source:

OpenAQ / environmental air quality monitoring datasets.

Contains:

timestamp  
aqi  
pm25  
location  

These datasets simulate environmental signals with potential anomaly conditions.

---

# 3. DATA INGESTION FLOW

The ingestion layer performs the following steps:

1. Load datasets from CSV files  
2. Normalize fields into NICAI signal schema  
3. Generate structured signals  
4. Inject variability and anomaly patterns  

Example signal:

```json
{
 "signal_id": "W_2",
 "timestamp": "2026-04-14T04:21:32",
 "latitude": 19.0760,
 "longitude": 72.8777,
 "value": 48.7,
 "dataset_id": "weather"
}
```

These signals are passed to the NICAI validation layer.

---

# 4. TRACEABILITY

Each signal is assigned a deterministic trace_id during validation.

Example generation logic:

trace_id = SHA256(signal_id + timestamp)

Trace IDs propagate through:

Validation → Intelligence Analysis → Pattern Detection → Dashboard → Action Routing

Example:

```json
{
 "signal_id": "W_2",
 "trace_id": "0ea1438a7f5bb3795e73fa6d2519b8ef..."
}
```

Traceability ensures every signal can be tracked across the entire system pipeline.

---

# 5. MULTI-SIGNAL INTELLIGENCE

NICAI performs grouped anomaly detection.

Signals are analyzed collectively using:

• location clustering  
• time window grouping  
• anomaly frequency analysis  

Example pattern output:

```json
{
 "pattern_id": "PATTERN_d2c00b",
 "anomaly_count": 5,
 "affected_zones": ["Zone_A"],
 "pattern_type": "CLUSTER_ANOMALY",
 "severity_trend": "INCREASING",
 "linked_traces": ["trace1","trace2","trace3"]
}
```

This ensures anomalies are detected as patterns instead of isolated signals.

---

# 6. LIVE SYSTEM FLOW

The NICAI system operates as:

1. Dataset ingested and converted into signals  
2. Signals processed through NICAI validation layer  
3. Intelligence engine detects anomalies  
4. Multi-signal analyzer detects patterns  
5. Results exposed through API endpoints  
6. Dashboard fetches signals and patterns  
7. User triggers action via dashboard  
8. Action payload logged with trace_id  

---

# 7. API ENDPOINTS

NICAI exposes the following API endpoints.

GET /signals

Returns processed signals.

Example response:

```json
[
 {
  "signal_id": "W_2",
  "status": "VALID",
  "confidence_score": 0.9,
  "trace_id": "...",
  "anomaly_score": 0.9,
  "risk_level": "HIGH",
  "anomaly_type": "TEMPERATURE_SPIKE",
  "explanation": "Extreme temperature detected",
  "recommendation_signal": "ESCALATE"
 }
]
```

GET /patterns

Returns detected anomaly patterns.

Example response:

```json
{
 "pattern_id": "PATTERN_d2c00b",
 "anomaly_count": 5,
 "pattern_type": "CLUSTER_ANOMALY"
}
```

POST /action

Logs dashboard-triggered action.

Example request:

```json
{
 "trace_id": "...",
 "action_type": "ESCALATE"
}
```

Example response:

```json
{
 "status": "action logged"
}
```

---

# 8. DASHBOARD TEST

Start dashboard server:

```
uvicorn dashboard:app --reload
```

Open browser:

```
http://127.0.0.1:8000
```

Dashboard displays:

• Signal ID  
• Validation Status  
• Risk Level  
• Anomaly Type  
• Explanation  
• Action Panel  

Action buttons:

Escalate  
Review  
Assign  

---

# 9. ACTION ROUTING

NICAI does not execute actions.

When a user clicks an action button, the system generates an action payload.

Example payload:

```json
{
 "trace_id": "...",
 "action_type": "ESCALATE",
 "target_role": "authority",
 "timestamp": "2026-04-14T04:21:32",
 "context": {
   "signal_id": "W_2",
   "anomaly_type": "TEMPERATURE_SPIKE",
   "pattern_id": "PATTERN_d2c00b"
 }
}
```

The payload is stored in:

```
action_logs.json
```

---

# 10. OBSERVABILITY

System observability is maintained through logs.

Primary log files:

action_logs.json  
telemetry_metrics.json  

These logs capture:

• action routing events  
• pipeline execution stages  
• system telemetry  

Logs are generated during testing.

---

# 11. FAILURE HANDLING

The system handles invalid inputs deterministically.

Example invalid signal conditions:

• missing timestamp  
• invalid coordinates  
• empty values  
• incorrect dataset ID  

Validation response example:

```json
{
 "signal_id": "W_25",
 "status": "REJECT",
 "reason": "missing timestamp"
}
```

Rejected signals do not proceed to analysis.

---

# 12. SUCCESS CRITERIA

The system passes testing if:

• datasets load successfully  
• signals process without crashes  
• anomaly detection works correctly  
• patterns are detected  
• dashboard displays intelligence outputs  
• action payloads generate correctly  
• logs capture system activity  

---

# 13. TEST READY

The NICAI system is ready for evaluation under the **BHIV Universal Testing Protocol**.

The system supports:

• deterministic processing  
• real dataset ingestion  
• anomaly intelligence generation  
• dashboard-based action routing  
• full traceability of signals