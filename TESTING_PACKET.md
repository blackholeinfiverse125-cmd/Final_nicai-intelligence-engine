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

These datasets simulate environmental signals with anomaly conditions.

---

# 3. DATA INGESTION FLOW

The ingestion layer performs:

1. Load datasets from CSV files
2. Normalize fields into NICAI signal schema
3. Generate structured signals
4. Inject variability and anomalies

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

---

# 4. TRACEABILITY

Each signal is assigned a deterministic trace_id.

Generation logic:

trace_id = SHA256(signal_id + timestamp)

Trace flow:

Validation → Analysis → Pattern Detection → Dashboard → Action Logs

Example:

```json
{
 "signal_id": "W_2",
 "trace_id": "0ea1438a7f5bb3795e73fa6d2519b8ef..."
}
```

---

# 5. MULTI-SIGNAL INTELLIGENCE

NICAI performs grouped anomaly detection using:

• location clustering
• anomaly frequency
• zone-based grouping

Example pattern output:

```json
{
 "pattern_id": "PATTERN_xxxx",
 "anomaly_count": 5,
 "affected_zones": ["Zone_A"],
 "pattern_type": "CLUSTER_ANOMALY",
 "severity_trend": "INCREASING",
 "linked_traces": ["trace1","trace2"]
}
```

---

# 6. LIVE SYSTEM FLOW

1. Dataset → Signals
2. Signals → Validation
3. Validation → Intelligence Analysis
4. Analysis → Pattern Detection
5. Output → API
6. API → Dashboard
7. User → Action Trigger
8. Action → Logs

---

# 7. API ENDPOINTS

### GET /signals

Returns processed signals.

Example:

```json
[
 {
  "signal_id": "W_2",
  "status": "VALID",
  "risk_level": "HIGH",
  "anomaly_type": "TEMPERATURE_SPIKE",
  "trace_id": "..."
 }
]
```

---

### GET /patterns

Returns multi-signal pattern output.

```json
{
 "pattern_id": "PATTERN_xxxx",
 "anomaly_count": 5,
 "affected_zones": ["Zone_A"],
 "pattern_type": "CLUSTER_ANOMALY",
 "severity_trend": "INCREASING",
 "linked_traces": ["..."]
}
```

---

### POST /action

Logs action from dashboard.

Request:

```json
{
 "trace_id": "...",
 "action_type": "ESCALATE",
 "context": {
   "signal_id": "W_2",
   "risk_level": "HIGH",
   "anomaly_type": "TEMPERATURE_SPIKE"
 }
}
```

Response:

```json
{
 "status": "action logged"
}
```

---

# 8. DASHBOARD TEST

Run:

```
uvicorn dashboard:app --reload
```

Open:

```
http://127.0.0.1:8000
```

Dashboard shows:

• Signal ID
• Zone
• Status
• Risk Level
• Anomaly Type
• Explanation
• Action Panel

---

# 9. API TESTING

Test endpoints:

```
http://127.0.0.1:8000/signals
http://127.0.0.1:8000/patterns
```

---

# 10. ACTION TESTING

Steps:

1. Click any action button
2. Open file:

```
action_logs.json
```

3. Verify:

• trace_id matches signal
• action_type correct
• context present

---

# 11. ACTION ROUTING

Example payload:

```json
{
 "trace_id": "...",
 "action_type": "ESCALATE",
 "target_role": "authority",
 "timestamp": "...",
 "context": {
   "signal_id": "W_2",
   "risk_level": "HIGH",
   "anomaly_type": "TEMPERATURE_SPIKE"
 }
}
```

---

# 12. OBSERVABILITY

Logs generated:

```
validation_logs.json
anomaly_logs.json
pattern_logs.json
action_logs.json
```

These track:

• validation events
• anomaly detection
• pattern detection
• user actions

---

# 13. FAILURE HANDLING

Invalid cases:

• missing timestamp
• invalid data
• null values
• invalid dataset

Example:

```json
{
 "signal_id": "W_25",
 "status": "REJECT",
 "reason": "missing timestamp"
}
```

Rejected signals stop processing.

---

# 14. SUCCESS CRITERIA

System passes if:

• data loads successfully
• no crashes
• anomalies detected
• patterns generated
• dashboard works
• actions logged
• logs verifiable

---

# 15. TEST READY

NICAI is ready for BHIV testing.

Supports:

• deterministic processing
• real data ingestion
• anomaly intelligence
• dashboard actions
• traceability
