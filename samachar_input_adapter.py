import pandas as pd


# -----------------------------
# 1️⃣ LOAD DATA
# -----------------------------
def load_data():
    try:
        weather = pd.read_csv("data/clean_weather.csv")
        aqi = pd.read_csv("data/clean_aqi.csv")

        print("✅ Data Loaded Successfully")
        return weather, aqi

    except Exception as e:
        print("❌ Error loading data:", e)
        return None, None


# -----------------------------
# 2️⃣ CONVERT TO NICAI SIGNALS
# -----------------------------
def convert_to_signals(weather, aqi):

    signals = []

    # -----------------------------
    # Weather signals
    # -----------------------------
    for i, row in weather.iterrows():

        # Handle missing values safely
        if pd.isna(row.get("temperature")):
            continue

        signals.append({
            "signal_id": f"W_{i}",
            "timestamp": str(row.get("date", "")),
            "latitude": float(row.get("latitude", 0.0)),   # better than fixed 0.0
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