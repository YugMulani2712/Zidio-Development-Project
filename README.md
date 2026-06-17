# RetailPulse

## AI-Powered Customer Analytics & Demand Forecasting Platform

RetailPulse is an end-to-end retail analytics and machine learning project built to analyze customer behavior, forecast product demand, optimize inventory decisions, monitor data drift, and deploy an interactive business dashboard.

The project uses retail transaction data to convert raw sales records into actionable business insights through EDA, customer segmentation, forecasting, churn prediction, inventory optimization, monitoring, Docker containerization, CI/CD, and cloud deployment.

---

## Live Demo

**Streamlit App:**
https://dharmmaniya-retailpulse.streamlit.app/

---

## Project Objectives

* Analyze retail sales, revenue trends, customers, products, and country-wise performance
* Clean and prepare business-ready retail transaction data
* Perform customer segmentation using RFM and clustering
* Build demand forecasting models using Prophet, LSTM, and hybrid forecasting
* Predict customer churn using machine learning
* Optimize inventory using safety stock, reorder point, EOQ, and stockout risk
* Monitor dataset drift and retraining requirements
* Build an interactive Streamlit dashboard
* Containerize the project using Docker
* Prepare Kubernetes deployment configuration
* Set up GitHub Actions CI/CD pipeline
* Deploy the final dashboard using Streamlit Community Cloud

---

## Tech Stack

| Area             | Tools                                  |
| ---------------- | -------------------------------------- |
| Programming      | Python                                 |
| Data Analysis    | Pandas, NumPy                          |
| Visualization    | Matplotlib, Seaborn, Altair, Streamlit |
| Machine Learning | Scikit-learn, XGBoost                  |
| Forecasting      | Prophet, LSTM                          |
| Deep Learning    | PyTorch Lightning                      |
| Monitoring       | Drift Detection, Retraining Logs       |
| Deployment       | Streamlit Cloud, Docker                |
| DevOps           | GitHub Actions, Kubernetes YAML        |
| Version Control  | Git, GitHub, Git LFS                   |

---

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
├── Reports/
│   ├── Figure/
│   ├── Model_Reports/
│   └── Drift_Reports/
│
├── Scripts/
│   ├── retailpulse_retrain.py
│   └── dag_airflow.py
│
├── k8s/
│   ├── deployment.yaml
│   └── service.yaml
│
├── .github/
│   └── workflows/
│       └── ci-cd.yml
│
├── Dockerfile
├── .dockerignore
├── requirements.txt
├── DEPLOYMENT.md
└── README.md
```

---

## Dataset Overview

The project is based on retail transaction data containing invoice-level sales records.

| Item              | Details                                                                                            |
| ----------------- | -------------------------------------------------------------------------------------------------- |
| Raw data size     | Around 1M+ rows                                                                                    |
| Cleaned data size | 779,425 rows                                                                                       |
| Time period       | 2009-12-01 to 2011-12-09                                                                           |
| Main columns      | Invoice, InvoiceDate, CustomerID, StockCode, Description, Quantity, UnitPrice, Country, TotalPrice |

Large data files are managed carefully because GitHub has file-size limits. Git LFS or local data storage is used for large CSV files.

---

## Main Modules

### 1. Exploratory Data Analysis

Performed initial data understanding, missing value analysis, duplicate checks, distribution analysis, sales trends, product-level analysis, and country-wise revenue analysis.

### 2. Data Cleaning

Cleaned invalid records, removed cancellations, returns, missing customer IDs, non-positive quantity/price rows, and duplicate transactions.

Final cleaned dataset:

```text
retail_sales_cleaned.csv
```

### 3. Customer Segmentation

Built RFM features and clustering-based customer segmentation using KMeans and DBSCAN.

Main customer features:

```text
Recency
Frequency
Monetary
AverageOrderValue
CustomerLifetimeDays
UniqueProducts
AvgQty
```

### 4. Demand Forecasting

Prepared daily sales and product demand data for forecasting.

Models used:

```text
Prophet
LSTM
Hybrid Forecasting
```

### 5. Churn Prediction

Built churn prediction features using customer transaction behavior and trained machine learning models for churn risk prediction.

### 6. Inventory Optimization

Calculated:

```text
Safety Stock
Reorder Point
EOQ
Days of Cover
Stockout Risk
Reorder Quantity
```

### 7. Drift Monitoring and Retraining

Implemented drift monitoring using statistical comparison between reference and current periods.

Retraining decision logic:

```text
If drift score is high → retraining required
If drift score is low/moderate → skip retraining
```

### 8. Streamlit Dashboard

Built an interactive dashboard with five pages:

```text
Sales Dashboard
Customer Dashboard
Forecast Dashboard
Inventory Dashboard
Monitoring Dashboard
```

---

## Key Results

| Module                 | Result                          |
| ---------------------- | ------------------------------- |
| Cleaned sales data     | 779,425 valid rows              |
| Prophet forecast       | WAPE 27.78%                     |
| LSTM baseline          | Underperformed, WAPE around 70% |
| Hybrid forecasting     | MAPE 20.57%                     |
| Churn prediction       | ROC-AUC 0.8129                  |
| Inventory optimization | 25.90% understock reduction     |
| Drift monitoring       | Drift score 0.33                |
| Retraining decision    | Skip retraining                 |

---

## Important Notes

### Forecasting

The hybrid forecasting model improved the forecasting pipeline, but the target MAPE was not fully reached due to demand spikes, irregular product-level sales, and limited tuning time.

### Churn Prediction

The churn model achieved ROC-AUC 0.8129 after removing leakage-based features. The final model uses transaction-based customer behavior features.

### Inventory Optimization

The inventory model achieved the understock reduction target. Overstock increased as a trade-off because higher safety stock was used to reduce stockout risk.

### Drift Monitoring

The drift score was 0.33, so retraining was skipped at this stage.

---

## Streamlit App

Run locally:

```bash
streamlit run app/main.py
```

Live deployment:

```text
https://dharmmaniya-retailpulse.streamlit.app/
```

---

## Docker Setup

Build Docker image:

```bash
docker build -t retailpulse .
```

Run Docker container:

```bash
docker run -p 8501:8501 retailpulse
```

Open:

```text
http://localhost:8501
```

Docker packages the Streamlit dashboard, dependencies, data files, and run command into one container.

---

## Kubernetes Setup

Kubernetes configuration files were prepared:

```text
k8s/deployment.yaml
k8s/service.yaml
```

Apply when Kubernetes is enabled:

```bash
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml
```

Kubernetes deployment was prepared for orchestration practice. Actual Kubernetes execution requires an active Kubernetes cluster.

---

## CI/CD Pipeline

GitHub Actions CI/CD pipeline was configured in:

```text
.github/workflows/ci-cd.yml
```

The pipeline checks:

```text
Python setup
Dependency installation
Important project files
Streamlit app syntax
```

This helps validate the project after every push or pull request to the main branch.

---

## Cloud Deployment

RetailPulse was deployed using Streamlit Community Cloud.

| Item       | Details                                        |
| ---------- | ---------------------------------------------- |
| Platform   | Streamlit Community Cloud                      |
| Repository | Dharm124/retailpulse-analytics                 |
| Branch     | main                                           |
| Entry file | app/main.py                                    |
| Live URL   | https://dharmmaniya-retailpulse.streamlit.app/ |

AWS/GCP deployment was not performed because it requires additional billing setup, container registry configuration, and cloud Kubernetes resources. Streamlit Cloud was selected as the most practical deployment option for this project.

---

## How to Run This Project

### 1. Clone Repository

```bash
git clone https://github.com/Dharm124/retailpulse-analytics.git
cd retailpulse-analytics
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Run Streamlit App

```bash
streamlit run app/main.py
```

### 4. Open Dashboard

```text
http://localhost:8501
```

---

## Final Project Status

| Component              | Status    |
| ---------------------- | --------- |
| EDA                    | Completed |
| Data Cleaning          | Completed |
| Customer Segmentation  | Completed |
| Forecasting            | Completed |
| Churn Prediction       | Completed |
| Inventory Optimization | Completed |
| Drift Monitoring       | Completed |
| Streamlit Dashboard    | Completed |
| Docker Setup           | Completed |
| Kubernetes Config      | Prepared  |
| CI/CD Pipeline         | Completed |
| Cloud Deployment       | Completed |
| Final QA               | Completed |

---

## Author

**Dharm Maniya**
B.Tech Artificial Intelligence and Data Science
Machine Learning & Data Science Project

---

## Conclusion

RetailPulse demonstrates a complete retail analytics and machine learning workflow from raw data processing to dashboard deployment.

The project covers data cleaning, customer analytics, demand forecasting, churn prediction, inventory optimization, monitoring, Docker containerization, CI/CD automation, and Streamlit Cloud deployment.

The final dashboard is publicly available at:

```text
https://dharmmaniya-retailpulse.streamlit.app/
```
