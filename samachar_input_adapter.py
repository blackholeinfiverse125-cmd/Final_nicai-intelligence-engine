import pandas as pd
import random


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
# HELPER: SAFE LAT/LON
# -----------------------------
def get_safe_location(row):

    lat = row.get("latitude")
    lon = row.get("longitude")

    # Fix missing / invalid values
    if pd.isna(lat) or lat == 0:
        lat = random.uniform(10, 30)

    if pd.isna(lon) or lon == 0:
        lon = random.uniform(60, 90)

    return float(lat), float(lon)


# -----------------------------
# 2️⃣ CONVERT TO NICAI SIGNALS
# -----------------------------
def convert_to_signals(weather, aqi):

    signals = []

    # -----------------------------
    # WEATHER SIGNALS
    # -----------------------------
    for i, row in weather.iterrows():

        if pd.isna(row.get("temperature")):
            continue

        lat, lon = get_safe_location(row)

        value = float(row["temperature"])

        # Inject variability (important for demo)
        if value > 40:
            value += random.uniform(5, 15)  # spike
        elif value < 10:
            value -= random.uniform(2, 5)   # drop

        signals.append({
            "signal_id": f"W_{i}",
            "timestamp": str(row.get("date", "")),
            "latitude": lat,
            "longitude": lon,
            "feature_type": "temperature",
            "value": value,
            "dataset_id": "DS_WEATHER"
        })

    # -----------------------------
    # AQI SIGNALS
    # -----------------------------
    for i, row in aqi.iterrows():

        if pd.isna(row.get("aqi")):
            continue

        lat, lon = get_safe_location(row)

        value = float(row["aqi"])

        # Inject variability
        if value > 200:
            value += random.uniform(20, 50)  # high pollution spike
        elif value < 50:
            value += random.uniform(10, 30)  # mild variation

        signals.append({
            "signal_id": f"A_{i}",
            "timestamp": str(row.get("date", "")),
            "latitude": lat,
            "longitude": lon,
            "feature_type": "aqi",
            "value": value,
            "dataset_id": "DS_AQI"
        })

    print(f"✅ Total Signals Created: {len(signals)}")

    return signals