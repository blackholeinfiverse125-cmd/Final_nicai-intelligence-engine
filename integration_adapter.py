from sanskar_engine import SanskarEngine

engine = SanskarEngine()

def map_input(data):
    return {
        "temperature": float(data.get("temperature", data.get("temp", 0))),
        "pollution": float(data.get("aqi", data.get("aqi_value", 0))),
        "trend": float(data.get("trend", 0.5)),
        "zone": [data.get("city", data.get("location", "unknown"))]
    }

def run_engine(data):
    signals = map_input(data)
    return engine.process(signals)