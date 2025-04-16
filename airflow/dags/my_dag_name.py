import datetime

from airflow import DAG
from airflow.operators.empty import EmptyOperator
from airflow.operators.python import PythonOperator

def my_function():
    return 1

def my_function2(a: int):
    print(a)
    return None

with DAG(
    dag_id="my_dag_name",
    start_date=datetime.datetime(2021, 1, 1),
    schedule="@daily",
    catchup=False,  # Boa prática para evitar execução retroativa se não for necessário
    tags=["exemplo"]
) as dag:

    task1 = EmptyOperator(task_id="task1")

    task2 = PythonOperator(
        task_id="task2",
        python_callable=my_function
    )

    task3 = PythonOperator(
        task_id="task3",
        python_callable=my_function2,
        op_args=[1]  # Aqui você pode passar argumentos fixos ou usar XCom
    )

    task4 = EmptyOperator(task_id="task4")

    _ = task1 >> task2 >> task3 >> task4
