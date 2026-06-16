
import streamlit as st
import pandas as pd
from utils import load_cleaned_data

st.set_page_config(page_title="Sales Dashboard",page_icon="💰",layout="wide")

st.title("💰 Sales Dashboard")
st.write("Sales performance overview based on cleaned retail transaction data.")

df = load_cleaned_data()

df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"])
df["Month"] = df["InvoiceDate"].dt.to_period("M").astype(str)

min_date = df["InvoiceDate"].min().date()
max_date = df["InvoiceDate"].max().date()

st.sidebar.header("🔎 Filters")
start_date = st.sidebar.date_input("Start Date",min_date)
end_date = st.sidebar.date_input("End Date",max_date)

filtered_df = df[
    (df["InvoiceDate"].dt.date >= start_date)
    &(df["InvoiceDate"].dt.date <= end_date)
]

total_revenue = filtered_df["TotalPrice"].sum()
total_orders = filtered_df["Invoice"].nunique()
total_customers = filtered_df["CustomerID"].nunique()
total_products = filtered_df["StockCode"].nunique()

col1,col2,col3,col4 = st.columns(4)

col1.metric("💵 Revenue",f"{total_revenue:,.0f}")
col2.metric("🧾 Orders",f"{total_orders:,}")
col3.metric("👥 Customers",f"{total_customers:,}")
col4.metric("📦 Products",f"{total_products:,}")

st.divider()

monthly_sales = filtered_df.groupby("Month")["TotalPrice"].sum().reset_index()
monthly_sales = monthly_sales.rename(columns={"TotalPrice":"Revenue"})

st.subheader("📈 Monthly Revenue Trend")
st.line_chart(monthly_sales,x="Month",y="Revenue")

col5,col6 = st.columns(2)

top_products = (
    filtered_df.groupby("Description")["TotalPrice"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
    .reset_index()
)

top_countries = (
    filtered_df.groupby("Country")["TotalPrice"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
    .reset_index()
)

with col5:
    st.subheader("🏆 Top 10 Products by Revenue")
    st.bar_chart(top_products,x="Description",y="TotalPrice")

with col6:
    st.subheader("🌍 Top 10 Countries by Revenue")
    st.bar_chart(top_countries,x="Country",y="TotalPrice")

st.subheader("🧾 Recent Transactions")
st.dataframe(
    filtered_df[["Invoice","InvoiceDate","CustomerID","StockCode","Description","Quantity","UnitPrice","TotalPrice","Country"]]
    .sort_values("InvoiceDate",ascending=False)
    .head(100),
    use_container_width=True
)
