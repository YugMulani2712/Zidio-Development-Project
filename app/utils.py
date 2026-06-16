from pathlib import Path
import pandas as pd
import streamlit as st

BASE_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = BASE_DIR / "Data" / "Processed"
REPORT =  BASE_DIR / "Reports" / "Model_Reports"

@st.cache_data
def load_cleaned_data():
    return pd.read_csv(DATA_DIR / "retail_sales_cleaned.csv",parse_dates=["InvoiceDate"])

@st.cache_data
def load_segments():
    return pd.read_csv(DATA_DIR / "retail_customer_segments.csv")

@st.cache_data
def load_demand_data():
    return pd.read_csv(DATA_DIR / "retail_product_daily_demand.csv",parse_dates=["Date"])

@st.cache_data
def load_churn_data():
    return pd.read_csv(DATA_DIR / "retail_churn_features.csv")

@st.cache_data
def load_inventory_data():
    return pd.read_csv(REPORT / "10-Inventory_Optimization.csv")