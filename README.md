# RetailPulse

RetailPulse is an end-to-end retail analytics and machine learning project built using the Online Retail II dataset.

The project covers data cleaning, exploratory data analysis, customer segmentation, demand forecasting, churn prediction, inventory optimization, drift detection, automated retraining logic, and a Streamlit dashboard.

## Project Objective

The main objective of RetailPulse is to build a complete retail intelligence system that helps analyze sales performance, customer behavior, demand patterns, inventory risk, and model monitoring status.

## Project Workflow

1. Data Collection
2. Data Cleaning
3. Exploratory Data Analysis
4. Customer Segmentation
5. Demand Forecasting
6. Hybrid Forecasting
7. Churn Prediction
8. Model Explainability
9. Hyperparameter Tuning
10. Inventory Optimization
11. Data Drift Detection
12. Automated Retraining Pipeline
13. Streamlit Dashboard

## Dataset

The project uses the Online Retail II dataset.

* Raw dataset: around 1 million transaction records
* Cleaned dataset: around 779K valid sales records
* Removed records include guest checkout rows, missing customer IDs, cancellations, returns, duplicates, and invalid quantity or price values.

## Key Results

| Module                 | Result                                |
| ---------------------- | ------------------------------------- |
| Prophet Forecasting    | WAPE 27.78%                           |
| LSTM Forecasting       | WAPE around 70%                       |
| Hybrid Forecasting     | MAPE 20.57%                           |
| Churn Prediction       | AUC-ROC 0.8129                        |
| Inventory Optimization | 25.90% estimated understock reduction |
| Data Drift Detection   | Drift score 0.33                      |
| Retraining Decision    | Skip retraining                       |

## Target Gap Summary

| Module              | Target                       | Achieved        | Reason                                                                                     |
| ------------------- | ---------------------------- | --------------- | ------------------------------------------------------------------------------------------ |
| LSTM Forecasting    | Better SKU-level forecasting | WAPE around 70% | SKU demand had many zero-sales days and sudden spikes                                      |
| Hybrid Forecasting  | MAPE ≤ 12%                   | MAPE 20.57%     | Hybrid improved results but target was not reached due to demand spikes and limited tuning |
| Churn Prediction    | AUC ≥ 0.88                   | AUC 0.8129      | Leakage features were removed, so only transaction-based features were used                |
| Inventory Optimization | Reduce understock by 25–40% | 25.90% understock reduction ✅ | Target achieved; overstock increased as a safety-stock trade-off |

## Streamlit Dashboard

The project includes a Streamlit dashboard with the following pages:

1. Sales Dashboard
2. Customer Dashboard
3. Forecast Dashboard
4. Inventory Dashboard
5. Monitoring Dashboard

## Dashboard Features

### Sales Dashboard

* Revenue KPIs
* Order and customer metrics
* Monthly revenue trend
* Top products
* Top countries
* Recent transaction records

### Customer Dashboard

* Customer segmentation overview
* RFM behavior
* Top customers
* Churn overview

### Forecast Dashboard

* SKU-level demand trend
* Top-selling SKU selection
* Forecasting model summary
* Demand records

### Inventory Dashboard

* EOQ
* Safety stock
* Reorder point
* Days of cover
* Stockout risk
* Inventory recommendation table

### Monitoring Dashboard

* Drift score
* Drifted feature count
* Retraining decision
* Drift summary
* Retraining log

## Project Structure

```text
RetailPulse/
├── app/
│   ├── main.py
│   ├── utils.py
│   └── pages/
│       ├── 1_Sales_Dashboard.py
│       ├── 2_Customer_Dashboard.py
│       ├── 3_Forecast_Dashboard.py
│       ├── 4_Inventory_Dashboard.py
│       └── 5_Monitoring_Dashboard.py
│
├── Data/
│   ├── Raw/
│   └── Processed/
│
├── Notebooks/
│
├── Reports/
│   ├── Figure/
│   ├── Model_Reports/
│   └── Drift_Reports/
│
├── Scripts/
│   ├── retailpulse_retrain.py
│   └── dag_airflow.py
│
├── requirements.txt
└── README.md
```

## How to Run the Project

Install required libraries:

```bash
pip install -r requirements.txt
```

Run the Streamlit dashboard:

```bash
streamlit run app/main.py
```

## Technologies Used

* Python
* Pandas
* NumPy
* Matplotlib
* Seaborn
* Scikit-learn
* XGBoost
* Optuna
* SHAP
* Prophet
* PyTorch
* Evidently
* Streamlit
* Airflow

## Final Status

RetailPulse is completed as a full retail analytics and machine learning pipeline.

The project includes data processing, machine learning models, inventory optimization, monitoring, automated retraining logic, and a working Streamlit dashboard.
