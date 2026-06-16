
import streamlit as st
import pandas as pd
from utils import load_segments,load_churn_data

st.set_page_config(page_title="Customer Dashboard",page_icon="👥",layout="wide")

st.title("👥 Customer Dashboard")
st.write("Customer segmentation, RFM behavior and churn overview.")

segment_df = load_segments()
churn_df = load_churn_data()

def get_col(df,options,default_name,default_value):
    for col in options:
        if col in df.columns:
            return col
    df[default_name] = default_value
    return default_name

segment_col = get_col(segment_df,["SegmentName","Persona","Segment_KMeans","Cluster","KMeansCluster"],"Segment","All Customers")
country_col = get_col(segment_df,["PrimaryCountry","Country"],"Country","Unknown")

st.sidebar.header("🔎 Filters")
countries = ["All"] + sorted(segment_df[country_col].dropna().astype(str).unique().tolist())
selected_country = st.sidebar.selectbox("Select Country",countries)

if selected_country != "All":
    segment_df = segment_df[segment_df[country_col].astype(str) == selected_country]

col1,col2,col3,col4 = st.columns(4)

col1.metric("👥 Customers",f"{segment_df['CustomerID'].nunique():,}")
col2.metric("📅 Avg Recency",f"{segment_df['Recency'].mean():.1f}")
col3.metric("🧾 Avg Frequency",f"{segment_df['Frequency'].mean():.1f}")
col4.metric("💰 Avg Monetary",f"{segment_df['Monetary'].mean():,.0f}")

st.divider()

col5,col6 = st.columns(2)

segment_count = segment_df[segment_col].astype(str).value_counts().reset_index()
segment_count.columns = ["Segment","Customers"]

country_count = segment_df[country_col].astype(str).value_counts().head(10).reset_index()
country_count.columns = ["Country","Customers"]

with col5:
    st.subheader("📊 Customer Segments")
    st.bar_chart(segment_count,x="Segment",y="Customers")

with col6:
    st.subheader("🌍 Top Countries by Customers")
    st.bar_chart(country_count,x="Country",y="Customers")

st.subheader("💎 Top Customers by Monetary Value")

show_cols = [
    col for col in [
        "CustomerID",country_col,"Recency","Frequency","Monetary",
        "AverageOrderValue","CustomerLifetimeDays",segment_col
    ]
    if col in segment_df.columns
]

top_customers = segment_df.sort_values("Monetary",ascending=False).head(20)
st.dataframe(top_customers[show_cols],use_container_width=True)

st.divider()

st.subheader("⚠️ Churn Overview")

if "Churned" in churn_df.columns:
    active_customers = (churn_df["Churned"] == 0).sum()
    churned_customers = (churn_df["Churned"] == 1).sum()
    churn_rate = churn_df["Churned"].mean()*100

    c1,c2,c3 = st.columns(3)
    c1.metric("✅ Active Customers",f"{active_customers:,}")
    c2.metric("⚠️ Churned Customers",f"{churned_customers:,}")
    c3.metric("📉 Churn Rate",f"{churn_rate:.2f}%")

    churn_count = churn_df["Churned"].map({0:"Active",1:"Churned"}).value_counts().reset_index()
    churn_count.columns = ["Status","Customers"]

    st.bar_chart(churn_count,x="Status",y="Customers")
else:
    st.info("Churned column not found in churn dataset.")

st.subheader("📋 Customer Data Sample")
st.dataframe(segment_df.head(100),use_container_width=True)
