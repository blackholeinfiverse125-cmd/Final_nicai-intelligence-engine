from sanskar_engine import SanskarEngine

engine = SanskarEngine()

def map_input(data):
    value = data.get("value") or {}

    return {
        "temperature": float(value.get("temperature", 0)),   # no fallback
        "pollution": float(value.get("aqi", 0)),             # exact mapping
        "trend": float(data.get("trend", 0.5)),
        "zone": [data.get("location", "unknown")]
    }

def run_engine(data):
    signals = map_input(data)
    return engine.process(signals)