from pathlib import Path
from datetime import datetime

import pandas as pd
from scipy.stats import ks_2samp



BASE_DIR = Path(__file__).resolve().parents[1]

DEMAND_FILE = BASE_DIR / "Data" / "Processed" / "retail_product_daily_demand.csv"
REPORT_DIR = BASE_DIR / "Reports" / "Drift_Reports"

REPORT_DIR.mkdir(parents=True,exist_ok=True)

MONITOR_COLS = [
    "units_sold","revenue","n_invoices",
    "units_roll_7","units_roll_14","units_roll_30",
    "units_lag_1","units_lag_7","units_lag_14"
]

DRIFT_THRESHOLD = 0.50

# 1. LOAD DATA

def load_data():
    df = pd.read_csv(DEMAND_FILE,parse_dates=["Date"])

    print("Dataset loaded successfully.")
    print("Rows:",len(df))

    return df


# 2. VALIDATE DATA

def validate_data(df):
    required_cols = ["Date","StockCode"]+MONITOR_COLS

    missing_cols = [
        col for col in required_cols
        if col not in df.columns
    ]

    if df.empty:
        raise ValueError("Dataset is empty.")

    if missing_cols:
        raise ValueError(f"Missing columns: {missing_cols}")

    print("Data validation passed.")


# 3. CALCULATE REAL DRIFT SCORE

def calculate_drift(df):
    df = df[df["Date"] < df["Date"].max()].copy()

    last_date = df["Date"].max()

    current_start = last_date-pd.Timedelta(days=59)
    reference_start = current_start-pd.Timedelta(days=60)

    reference_df = df[
        (df["Date"] >= reference_start)
        &(df["Date"] < current_start)
    ]

    current_df = df[
        df["Date"] >= current_start
    ]

    drift_results = []

    for col in MONITOR_COLS:
        _,p_value = ks_2samp(
            reference_df[col].dropna(),
            current_df[col].dropna()
        )

        drift_results.append({
            "Feature":col,
            "P_Value":round(p_value,4),
            "Drifted":p_value < 0.05
        })

    drift_df = pd.DataFrame(drift_results)

    drift_score = drift_df["Drifted"].mean()

    return drift_df,drift_score


# 4. SAVE REPORTS AND PIPELINE LOG

def save_results(drift_df,drift_score):
    drift_df.to_csv(
        REPORT_DIR / "13-Drift_Summary.csv",
        index=False
    )

    decision = (
        "Retrain model"
        if drift_score >= DRIFT_THRESHOLD
        else "Skip retraining"
    )

    log_row = pd.DataFrame([{
        "RunDate":datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "DriftScore":round(drift_score,2),
        "DriftedColumns":int(drift_df["Drifted"].sum()),
        "TotalColumns":len(MONITOR_COLS),
        "Threshold":DRIFT_THRESHOLD,
        "Decision":decision
    }])

    log_file = REPORT_DIR / "13-Retraining_Log.csv"

    if log_file.exists():
        old_log = pd.read_csv(log_file)
        log_row = pd.concat([old_log,log_row],ignore_index=True)

    log_row.to_csv(log_file,index=False)

    print("Reports saved successfully.")

    return decision

# 5. RUN COMPLETE PIPELINE

def run_pipeline():
    print("RetailPulse pipeline started.\n")

    df = load_data()

    validate_data(df)

    drift_df,drift_score = calculate_drift(df)

    decision = save_results(drift_df,drift_score)

    print("\nDrift summary:")
    print(drift_df)

    print("\nDrift score:",round(drift_score,2))
    print("Drifted columns:",drift_df["Drifted"].sum(),"/",len(MONITOR_COLS))
    print("Decision:",decision)

    if drift_score >= DRIFT_THRESHOLD:
        print("Retraining trigger activated.")
    else:
        print("Existing models remain active.")


if __name__ == "__main__":
    run_pipeline()