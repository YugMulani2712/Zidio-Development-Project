
import streamlit as st
import pandas as pd
from utils import load_demand_data

st.set_page_config(page_title="Forecast Dashboard",page_icon="📈",layout="wide")

st.title("📈 Forecast Dashboard")
st.write("SKU-level demand trend and forecasting model summary.")

df = load_demand_data()
df["Date"] = pd.to_datetime(df["Date"])

st.sidebar.header("🔎 Filters")

sku_list = sorted(df["StockCode"].astype(str).unique())
selected_sku = st.sidebar.selectbox("Select SKU",sku_list)

sku_df = df[df["StockCode"].astype(str) == selected_sku].copy()

min_date = sku_df["Date"].min().date()
max_date = sku_df["Date"].max().date()

start_date = st.sidebar.date_input("Start Date",min_date)
end_date = st.sidebar.date_input("End Date",max_date)

sku_df = sku_df[
    (sku_df["Date"].dt.date >= start_date)
    &(sku_df["Date"].dt.date <= end_date)
]

total_units = sku_df["units_sold"].sum()
avg_units = sku_df["units_sold"].mean()
max_units = sku_df["units_sold"].max()
total_revenue = sku_df["revenue"].sum()

col1,col2,col3,col4 = st.columns(4)

col1.metric("📦 Total Units",f"{total_units:,.0f}")
col2.metric("📊 Avg Daily Units",f"{avg_units:.2f}")
col3.metric("🚀 Max Daily Units",f"{max_units:,.0f}")
col4.metric("💰 Revenue",f"{total_revenue:,.0f}")

st.divider()

st.subheader("📉 SKU Demand Trend")

chart_cols = ["Date","units_sold"]

if "units_roll_7" in sku_df.columns:
    chart_cols.append("units_roll_7")

if "units_roll_14" in sku_df.columns:
    chart_cols.append("units_roll_14")

trend_df = sku_df[chart_cols].set_index("Date")
st.line_chart(trend_df)

st.subheader("📋 Forecasting Model Summary")

model_summary = pd.DataFrame([
    ["Prophet Baseline","Business-level forecasting","WAPE 27.78%","Stable baseline"],
    ["LSTM Baseline","SKU-level forecasting","WAPE ~70%","Weak due to noisy SKU demand"],
    ["Hybrid Forecasting","Prophet + LSTM blending","MAPE 20.57%","Improved but target not reached"]
],columns=["Model","Purpose","Result","Status"])

st.dataframe(model_summary,use_container_width=True)

st.subheader("📊 Recent Demand Records")
st.dataframe(
    sku_df.sort_values("Date",ascending=False).head(100),
    use_container_width=True
)
