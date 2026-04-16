import pandas as pd
import os


# -----------------------------
# 1️⃣ LOAD DATA
# -----------------------------
def load_data():
    try:
        base_path = os.getcwd()

        weather_path = os.path.join(base_path, "clean_weather.csv")
        aqi_path = os.path.join(base_path, "clean_aqi.csv")

        weather = pd.read_csv(weather_path)
        aqi = pd.read_csv(aqi_path)

        print("✅ Data Loaded Successfully")
        return weather, aqi

    except Exception as e:
        print("❌ Error loading data:", e)
        return None, None


# -----------------------------
# 2️⃣ CONVERT TO NICAI SIGNALS
# -----------------------------
def convert_to_signals(weather, aqi):

    # ✅ SAFETY CHECK
    if weather is None or aqi is None:
        print("❌ Data is None, cannot convert signals")
        return []

    signals = []

    # -----------------------------
    # Weather signals
    # -----------------------------
    for i, row in weather.iterrows():

        if pd.isna(row.get("temperature")):
            continue

        signals.append({
            "signal_id": f"W_{i}",
            "timestamp": str(row.get("date", "")),
            "latitude": float(row.get("latitude", 0.0)),
            "longitude": float(row.get("longitude", 0.0)),
            "feature_type": "temperature",
            "value": float(row["temperature"]),
            "dataset_id": "DS_WEATHER"
        })

    # -----------------------------
    # AQI signals
    # -----------------------------
    for i, row in aqi.iterrows():

        if pd.isna(row.get("aqi")):
            continue

        signals.append({
            "signal_id": f"A_{i}",
            "timestamp": str(row.get("date", "")),
            "latitude": float(row.get("latitude", 0.0)),
            "longitude": float(row.get("longitude", 0.0)),
            "feature_type": "aqi",
            "value": float(row["aqi"]),
            "dataset_id": "DS_AQI"
        })

    print(f"✅ Total Signals Created: {len(signals)}")

    return signals
