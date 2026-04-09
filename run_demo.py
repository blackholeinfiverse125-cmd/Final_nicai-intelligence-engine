from validator import validate_signal
from sanskar_stub import analyze_signal
from decision_engine_stub import make_decision

signals = [
{
 "signal_id":"SIG100",
 "timestamp":"2026-03-10T10:00:00Z",
 "latitude":19.07,
 "longitude":72.87,
 "feature_type":"weather",
 "value":30,
 "dataset_id":"DS01"
},
{
 "signal_id":"SIG101",
 "timestamp":"2026-03-10T10:00:00Z",
 "latitude":18.5,
 "longitude":73.8,
 "feature_type":"vessel",
 "value":120,
 "dataset_id":"DS02"
}
]

for signal in signals:

    print("\nINPUT:", signal)

    validation = validate_signal(signal)
    print("VALIDATION:", validation)

    if validation["status"] == "REJECT":
        continue

    analytics = analyze_signal(validation)
    print("ANALYTICS:", analytics)

    decision = make_decision(analytics)
    print("DECISION:", decision)