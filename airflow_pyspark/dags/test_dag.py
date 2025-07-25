
from airflow.models.dag import DAG
from airflow.operators.bash import BashOperator
from airflow.utils.dates import days_ago

with DAG(
    dag_id='test_dag',
    start_date=days_ago(1),
    schedule_interval=None,
    tags=['test'],
) as dag:
    BashOperator(
        task_id='test_task',
        bash_command='echo "Test DAG ran successfully!"',
    )
