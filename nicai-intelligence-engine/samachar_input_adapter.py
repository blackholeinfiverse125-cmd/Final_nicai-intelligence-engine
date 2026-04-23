import pandas as pd


# -----------------------------
# 1️ LOAD DATA
# -----------------------------
def load_data():
    try:
        weather = pd.read_csv("clean_weather.csv")
        aqi = pd.read_csv("clean_aqi.csv")

        print(" Data Loaded Successfully")
        return weather, aqi

    except Exception as e:
        print("❌ Error loading data:", e)
        return None, None


# -----------------------------
# 2️ CONVERT TO NICAI SIGNALS
# -----------------------------
def convert_to_signals(weather, aqi):

    signals = []

    min_len = min(len(weather), len(aqi))

    for i in range(min_len):

        w = weather.iloc[i]
        a = aqi.iloc[i]

        if pd.isna(w.get("temperature")) or pd.isna(a.get("aqi")):
            continue

        signals.append({
            "signal_id": f"S_{i}",
            "timestamp": str(w.get("date", "2024-01-01T10:00:00")),

            # Correct NICAI structure
            "value": {
                "temperature": float(w["temperature"]),
                "aqi": float(a["aqi"])
            },

            "location": w.get("city", "unknown")
        })

    print(f" Combined Signals Created: {len(signals)}")

    return signals