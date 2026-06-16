import streamlit as st
from utils import load_cleaned_data,load_segments,load_demand_data,load_churn_data

st.set_page_config(
    page_title="RetailPulse Dashboard",
    page_icon="📊",
    layout="wide"
)

st.title("📊 RetailPulse Dashboard")
st.write("Retail analytics dashboard for sales, customers, forecasting, churn, inventory and monitoring.")

sales_df = load_cleaned_data()
segment_df = load_segments()
demand_df = load_demand_data()
churn_df = load_churn_data()

col1,col2,col3,col4 = st.columns(4)

col1.metric("Total Sales Rows",f"{len(sales_df):,}")
col2.metric("Customers",f"{sales_df['CustomerID'].nunique():,}")
col3.metric("Products",f"{sales_df['StockCode'].nunique():,}")
col4.metric("Churn Records",f"{len(churn_df):,}")

st.subheader("Project Modules Completed")

st.success("✅ Data Cleaning")
st.success("✅ EDA")
st.success("✅ Customer Segmentation")
st.success("✅ Forecasting")
st.success("✅ Churn Prediction")
st.success("✅ Inventory Optimization")
st.success("✅ Drift Detection")
st.success("✅ Retraining Pipeline")

st.info("Dashboard pages will be added one by one from the next days.")