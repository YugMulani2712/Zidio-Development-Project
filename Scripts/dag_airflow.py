from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime,timedelta
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(PROJECT_ROOT / "Scripts"))

from retailpulse_retrain import run_pipeline

default_args = {
    "owner":"retailpulse",
    "retries":1,
    "retry_delay":timedelta(minutes=5)
}

with DAG(
    dag_id="retailpulse_retraining_pipeline",
    default_args=default_args,
    start_date=datetime(2025,1,1),
    schedule="@weekly",
    catchup=False,
    tags=["retailpulse","mlops","drift-monitoring"]
) as dag:

    run_retraining_pipeline = PythonOperator(
        task_id="run_retraining_pipeline",
        python_callable=run_pipeline
    )

    run_retraining_pipeline