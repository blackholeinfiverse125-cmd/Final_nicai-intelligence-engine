import pandas as pd


# -----------------------------
# 1️⃣ LOAD DATA
# -----------------------------
def load_data():
    try:
        weather = pd.read_csv("clean_weather.csv")
        aqi = pd.read_csv("clean_aqi.csv")

        print("✅ Data Loaded Successfully")
        print("Weather rows:", len(weather))
        print("AQI rows:", len(aqi))

        return weather, aqi

    except Exception as e:
        print("❌ Error loading data:", e)
        return None, None


# -----------------------------
# 2️⃣ CONVERT TO NICAI SIGNALS
# -----------------------------
def convert_to_signals(weather, aqi):

    if weather is None or aqi is None:
        print("❌ Data not loaded")
        return []

    signals = []

    # -----------------------------
    # Weather signals
    # -----------------------------
    for i, row in weather.iterrows():

        # SAFE column extraction (NO "or" bug)
        temp = row.get("temperature")
        if temp is None:
            temp = row.get("temp")
        if temp is None:
            temp = row.get("Temperature")

        if pd.isna(temp):
            continue

        signals.append({
            "signal_id": f"W_{i}",
            "timestamp": str(row.get("date", "")),
            "latitude": float(row.get("latitude", 0.0)),
            "longitude": float(row.get("longitude", 0.0)),
            "feature_type": "temperature",
            "value": float(temp),
            "dataset_id": "DS_WEATHER"
        })

    # -----------------------------
    # AQI signals
    # -----------------------------
    for i, row in aqi.iterrows():

        aqi_val = row.get("aqi")
        if aqi_val is None:
            aqi_val = row.get("AQI")

        if pd.isna(aqi_val):
            continue

        signals.append({
            "signal_id": f"A_{i}",
            "timestamp": str(row.get("date", "")),
            "latitude": float(row.get("latitude", 0.0)),
            "longitude": float(row.get("longitude", 0.0)),
            "feature_type": "aqi",
            "value": float(aqi_val),
            "dataset_id": "DS_AQI"
        })

    print(f"✅ Total Signals Created: {len(signals)}")

    return signals
