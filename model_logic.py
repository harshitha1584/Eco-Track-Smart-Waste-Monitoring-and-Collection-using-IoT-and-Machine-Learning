# ======================
# 1. Imports
# ======================
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from statsmodels.tsa.arima.model import ARIMA
import matplotlib.pyplot as plt
from pmdarima import auto_arima

import warnings
warnings.filterwarnings("ignore")  # To suppress ARIMA fitting warnings

# Load dataset
df = pd.read_csv("EcoTrack_Waste_Bins_Dataset.csv")

# Parse dates
df["Start_Date"] = pd.to_datetime(df["Start_Date"], format="%d-%m-%Y", errors="coerce")
df["End_Date(100%)"] = pd.to_datetime(df["End_Date(100%)"], format="%d-%m-%Y", errors="coerce")
df["Fullness_80%_Date"] = pd.to_datetime(df["Fullness_80%_Date"], format="%d-%m-%Y", errors="coerce")


# -----------------------
# Train per-bin model
# -----------------------
def train_arima_for_bin(bin_id):
    """Train Auto ARIMA on Fill Duration of one bin."""
    g = df[df["Bin_ID"] == bin_id].sort_values("Start_Date")
    series = g["Fill_Duration(days)"].astype(float).rolling(window=3, min_periods=1).mean()


    if len(series) < 5:  # not enough data
        return None

    try:
        # Auto ARIMA automatically selects (p,d,q)
        model_fit = auto_arima(series, seasonal=False, stepwise=True, suppress_warnings=True)
        return model_fit
    except Exception as e:
        print(f"⚠️ ARIMA failed for {bin_id}: {e}")
        return None

def predict_for_location_zone(start_date_str, location_name, zone_type):
    start_dt = datetime.strptime(start_date_str, "%d-%m-%Y")
    
    # Filter bins in location and zone
    subset = df[(df["Location_Name"] == location_name) & (df["Zone_Type"] == zone_type)]
    unique_bins = subset["Bin_ID"].unique().tolist()

    # Zone-level time series (for fallback)
    zone_series = df[df["Zone_Type"] == zone_type]["Fill_Duration(days)"].groupby(df["Start_Date"]).mean()

    # Zone average duration (fallback)
    zone_avg = int(round(zone_series.mean()))

    results = []
    for bin_id in unique_bins:
        model_fit = train_arima_for_bin(bin_id)

        if model_fit is None:
            pred_days = zone_avg
        else:
            forecast = model_fit.predict(n_periods=1)
            forecast_value = float(np.array(forecast)[0])
            pred_days = max(1, int(round(forecast_value)))

        # Predicted dates
        pred_80 = start_dt + timedelta(days=max(1, pred_days - 2))
        pred_100 = start_dt + timedelta(days=pred_days)

        results.append({
            "Bin_ID": bin_id,
            "Start_Date": start_date_str,
            "Location_Name": location_name,
            "Zone_Type": zone_type,
            "Predicted_Fill_Duration(days)": pred_days,
            "Predicted_80pct_Date": pred_80.strftime("%d-%m-%Y"),
            "Predicted_100pct_Date": pred_100.strftime("%d-%m-%Y")
        })

    return pd.DataFrame(results)


# ======================
# 4. Visualization Functions (Updated: Compare Actual vs Predicted)
# ======================

# Plot predictions for all bins in a location/zone (Actual vs Predicted comparison - Line Chart)
def plot_predictions(start_date_str, location, zone):
    out = predict_for_location_zone(start_date_str, location, zone)
    if out.empty:
        print("No predictions available.")
        return

    # Compute actuals (last observed durations)
    actuals = []
    for b in out["Bin_ID"]:
        g = df[df["Bin_ID"] == b].sort_values("Start_Date")
        if not g.empty:
            actuals.append(g["Fill_Duration(days)"].values[-1])  # last actual duration
        else:
            actuals.append(None)
    out["Actual_Fill_Duration(days)"] = actuals

    # Line chart: Actual vs Predicted
    plt.figure(figsize=(10,5))
    x = range(len(out["Bin_ID"]))
    plt.plot(x, out["Actual_Fill_Duration(days)"], marker="o", label="Actual", color="blue")
    plt.plot(x, out["Predicted_Fill_Duration(days)"], marker="x", linestyle="--", label="Predicted", color="red")

    plt.xticks(x, out["Bin_ID"], rotation=90)
    plt.title(f"Actual vs Predicted Fill Durations - {location} ({zone})")
    plt.xlabel("Bin_ID")
    plt.ylabel("Fill Duration (days)")
    plt.legend()
    plt.tight_layout()
    plt.show()

    return out  # optional: return dataframe



