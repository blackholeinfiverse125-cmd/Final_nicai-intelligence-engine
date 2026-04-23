required_top_fields = [
    "signal_id",
    "timestamp",
    "value"
]

required_value_fields = [
    "temperature",
    "aqi"
]

field_types = {
    "signal_id": str,
    "timestamp": str,
    "value": dict,
    "temperature": (int, float),
    "aqi": (int, float),
    "location": str
}