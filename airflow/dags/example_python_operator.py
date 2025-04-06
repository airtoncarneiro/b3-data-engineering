from datetime import datetime
from airflow import DAG
from airflow.operators.python import PythonOperator
from time import sleep

def expensive_api_call():
    sleep(1000)
    return "API response"

with DAG(
    'example_python_operator',
    start_date=datetime(2023, 1, 1),
    schedule_interval=None
) as dag:
    
    task = PythonOperator(
        task_id='expensive_api_call',
        python_callable=expensive_api_call
    )
