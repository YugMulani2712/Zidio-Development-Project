
import streamlit as st
import pandas as pd
from pathlib import Path

st.set_page_config(page_title="Monitoring Dashboard",page_icon="🛰️",layout="wide")

st.title("🛰️ Monitoring Dashboard")
st.write("Data drift monitoring and retraining pipeline status.")

BASE_DIR = Path(__file__).resolve().parents[2]
DRIFT_DIR = BASE_DIR / "Reports" / "Drift_Reports"

drift_file = DRIFT_DIR / "13-Drift_Summary.csv"
log_file = DRIFT_DIR / "13-Retraining_Log.csv"

if not drift_file.exists():
    st.error("Drift summary file not found.")
    st.stop()

if not log_file.exists():
    st.error("Retraining log file not found.")
    st.stop()

drift_df = pd.read_csv(drift_file)
log_df = pd.read_csv(log_file)

latest_log = log_df.tail(1).iloc[0]

drift_score = latest_log["DriftScore"]
drifted_columns = latest_log["DriftedColumns"]
total_columns = latest_log["TotalColumns"]
decision = latest_log["Decision"]

col1,col2,col3,col4 = st.columns(4)

col1.metric("📊 Drift Score",drift_score)
col2.metric("⚠️ Drifted Columns",f"{drifted_columns}/{total_columns}")
col3.metric("🎯 Threshold",latest_log["Threshold"])
col4.metric("🔁 Decision",decision)

if decision == "Skip retraining":
    st.success("✅ Current drift is below threshold. Existing models remain active.")
else:
    st.warning("⚠️ Drift exceeded threshold. Retraining is required.")

st.divider()

col5,col6 = st.columns(2)

drift_status = drift_df["Drifted"].value_counts().reset_index()
drift_status.columns = ["Drifted","Count"]
drift_status["Drifted"] = drift_status["Drifted"].map({True:"Drifted",False:"Not Drifted"})

with col5:
    st.subheader("📌 Drift Status Count")
    st.bar_chart(drift_status,x="Drifted",y="Count")

with col6:
    st.subheader("📉 Feature P-Values")
    pvalue_df = drift_df[["Feature","P_Value"]].set_index("Feature")
    st.bar_chart(pvalue_df)

st.subheader("📋 Drift Summary")
st.dataframe(drift_df,use_container_width=True)

st.subheader("🧾 Retraining Log")
st.dataframe(log_df.sort_values("RunDate",ascending=False),use_container_width=True)

st.subheader("📌 Monitoring Notes")

notes_df = pd.DataFrame([
    ["Drift Score","Share of monitored features that are drifted"],
    ["P-Value","Low p-value means feature distribution changed"],
    ["Threshold","Retraining starts when drift score reaches 0.50 or higher"],
    ["Current Decision","Models remain active because current drift is below threshold"]
],columns=["Term","Meaning"])

st.dataframe(notes_df,use_container_width=True)
