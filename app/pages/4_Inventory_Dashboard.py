
import streamlit as st
import pandas as pd
from utils import load_inventory_data
import altair as alt

st.set_page_config(page_title="Inventory Dashboard",page_icon="📦",layout="wide")

st.title("📦 Inventory Dashboard")
st.write("Inventory optimization overview using EOQ, safety stock, reorder point and stockout risk.")

df = load_inventory_data()

required_cols = ["StockCode","avg_daily_demand","safety_stock","reorder_point","eoq","days_of_cover","stockout_risk","needs_reorder","reorder_qty"]

missing = [col for col in required_cols if col not in df.columns]

if missing:
    st.error(f"Missing columns: {missing}")
    st.stop()

st.sidebar.header("🔎 Filters")

risk_options = ["All"] + sorted(df["stockout_risk"].dropna().astype(str).unique().tolist())
selected_risk = st.sidebar.selectbox("Stockout Risk",risk_options)

filtered_df = df.copy()

if selected_risk != "All":
    filtered_df = filtered_df[filtered_df["stockout_risk"].astype(str) == selected_risk]

reorder_flag = filtered_df["needs_reorder"].astype(str).str.lower().isin(["true","1","yes"])

total_skus = filtered_df["StockCode"].nunique()
reorder_skus = reorder_flag.sum()
avg_days_cover = filtered_df["days_of_cover"].mean()
avg_safety_stock = filtered_df["safety_stock"].mean()

col1,col2,col3,col4 = st.columns(4)

col1.metric("📦 Total SKUs",f"{total_skus:,}")
col2.metric("🔁 Reorder SKUs",f"{reorder_skus:,}")
col3.metric("📅 Avg Days Cover",f"{avg_days_cover:.1f}")
col4.metric("🛡️ Avg Safety Stock",f"{avg_safety_stock:.1f}")

st.divider()

col5,col6 = st.columns(2)

risk_count = filtered_df["stockout_risk"].astype(str).value_counts().reset_index()
risk_count.columns = ["Risk","SKUs"]

priority_skus = (
    filtered_df.sort_values("days_of_cover",ascending=True)
    .head(10)[["StockCode","days_of_cover"]]
)

with col5:
    st.subheader("⚠️ Stockout Risk Count")
    
    risk_chart = alt.Chart(risk_count).mark_bar().encode(
        x=alt.X("SKUs:Q",title="Number of SKUs"),
        y=alt.Y("Risk:N",title="Risk Level"),
        tooltip=["Risk","SKUs"]
    ).properties(height=180)

    st.altair_chart(risk_chart,use_container_width=True)
    st.caption("All selected SKUs are currently classified as Medium Risk.")

with col6:
    st.subheader("📉 Lowest Days of Cover SKUs")
    st.bar_chart(priority_skus,x="StockCode",y="days_of_cover")

st.subheader("📋 Inventory Recommendation Table")

show_cols = [
    "StockCode","avg_daily_demand","safety_stock","reorder_point",
    "eoq","days_of_cover","stockout_risk","needs_reorder","reorder_qty"
]

st.dataframe(
    filtered_df[show_cols].sort_values("reorder_qty",ascending=False),
    use_container_width=True
)

st.subheader("📌 Inventory Model Summary")

summary_df = pd.DataFrame([
    ["EOQ","Find ideal order quantity"],
    ["Safety Stock","Protect against demand uncertainty"],
    ["Reorder Point","Decide when to reorder inventory"],
    ["Days of Cover","Estimate how long current stock can support demand"],
    ["Stockout Risk","Identify products with shortage risk"]
],columns=["Concept","Purpose"])

st.dataframe(summary_df,use_container_width=True)
