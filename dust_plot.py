import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from scipy.ndimage import median_filter

# ─────────────────────────────────────────────
# CONFIGURATION — adjust to match your Excel file
# ─────────────────────────────────────────────
EXCEL_FILE = "your_data.xlsx"   # <-- change to your file name/path

# Column names in your Excel sheet (change if different)
TIME_COL      = "Time"           # e.g., "Time" or "Timestamp"
ADC_COL       = "ADC"            # e.g., "ADC Value" or "Voltage"
DUST_COL      = "Dust Density"   # e.g., "Dust Density" or "mg/m3"
DATASET_COL   = "Dataset"        # column that labels "Morning" / "Evening"
                                 # If no such column exists, set SPLIT_BY_ROW = True

# If your file has no "Morning/Evening" label column, set this True
# and provide approximate row index where evening data starts
SPLIT_BY_ROW    = False
EVENING_ROW_START = 200          # used only if SPLIT_BY_ROW = True

# Filter parameters
MEDIAN_KERNEL   = 5   # window size for median filter (odd number)
MOVING_AVG_WIN  = 10  # window size for moving average

# ─────────────────────────────────────────────
# LOAD DATA
# ─────────────────────────────────────────────
print(f"Loading {EXCEL_FILE} ...")
all_sheets = pd.read_excel(EXCEL_FILE, sheet_name=None)
print(f"Sheets found: {list(all_sheets.keys())}")

# Combine all sheets into one dataframe (or pick a specific sheet)
df = pd.concat(all_sheets.values(), ignore_index=True)

print("Columns detected:", df.columns.tolist())
print(df.head())

# ─────────────────────────────────────────────
# SORT DATA
# ─────────────────────────────────────────────
df[TIME_COL] = pd.to_datetime(df[TIME_COL], errors='coerce')
df = df.dropna(subset=[TIME_COL])
df = df.sort_values(TIME_COL).reset_index(drop=True)

# Save sorted Excel
sorted_path = EXCEL_FILE.replace(".xlsx", "_sorted.xlsx")
with pd.ExcelWriter(sorted_path, engine='openpyxl') as writer:
    df.to_excel(writer, index=False, sheet_name="Sorted Data")
print(f"Sorted data saved to: {sorted_path}")

# ─────────────────────────────────────────────
# SPLIT MORNING / EVENING
# ─────────────────────────────────────────────
if SPLIT_BY_ROW:
    df_morning = df.iloc[:EVENING_ROW_START].copy()
    df_evening = df.iloc[EVENING_ROW_START:].copy()
else:
    # Try to detect by DATASET_COL or by time-of-day
    if DATASET_COL in df.columns:
        labels = df[DATASET_COL].str.lower()
        df_morning = df[labels.str.contains("morning", na=False)].copy()
        df_evening = df[labels.str.contains("evening", na=False)].copy()
    else:
        # Auto-split by hour: morning = 5:00–12:00, evening = 12:01–22:00
        hour = df[TIME_COL].dt.hour
        df_morning = df[hour < 12].copy()
        df_evening = df[hour >= 12].copy()

print(f"Morning rows: {len(df_morning)}, Evening rows: {len(df_evening)}")

# ─────────────────────────────────────────────
# FILTER FUNCTION
# ─────────────────────────────────────────────
def apply_filters(series, med_k=MEDIAN_KERNEL, avg_w=MOVING_AVG_WIN):
    med = median_filter(series.values, size=med_k)
    avg = pd.Series(med).rolling(window=avg_w, center=True, min_periods=1).mean().values
    return med, avg

# ─────────────────────────────────────────────
# PLOT
# ─────────────────────────────────────────────
fig, axes = plt.subplots(2, 1, figsize=(14, 10), sharex=False)
fig.suptitle("Dust Concentration vs Time\n(Raw + Median-Moving Average Filter)",
             fontsize=14, fontweight='bold')

datasets = [
    (df_morning, axes[0], "Morning",  "#1f77b4", "#ff7f0e"),
    (df_evening, axes[1], "Evening",  "#2ca02c", "#d62728"),
]

for df_set, ax, label, raw_color, filt_color in datasets:
    if df_set.empty:
        ax.set_title(f"{label} — No data found")
        continue

    x   = df_set[TIME_COL]
    raw = df_set[DUST_COL].values

    med_vals, avg_vals = apply_filters(pd.Series(raw))

    ax.plot(x, raw,      color=raw_color,  alpha=0.4, linewidth=0.8, label="Raw")
    ax.plot(x, avg_vals, color=filt_color, linewidth=2.0,            label=f"Median+MovAvg (k={MEDIAN_KERNEL}, w={MOVING_AVG_WIN})")

    ax.set_title(f"{label} Session", fontsize=12)
    ax.set_ylabel("Dust Concentration (mg/m³)")
    ax.set_xlabel("Time")
    ax.legend(loc="upper right")
    ax.grid(True, alpha=0.3)
    ax.tick_params(axis='x', rotation=30)

plt.tight_layout()
out_png = "dust_concentration_plot.png"
plt.savefig(out_png, dpi=150, bbox_inches='tight')
print(f"Plot saved to: {out_png}")
plt.show()
