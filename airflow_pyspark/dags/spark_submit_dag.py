from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.utils.dates import days_ago

default_args = {
    'owner': 'Harry Song',
    'retries': 3,
}

with DAG(
    dag_id='spark_dag_bash',
    default_args=default_args,
    start_date=days_ago(1),
    schedule_interval='@daily',
    catchup=False,
    tags=['spark', 'bash'],
) as dag:
    run_spark_job = BashOperator(
        task_id='run_spark_app',
        bash_command="""
            docker run --rm \
            --network airflow_pyspark_mynet \
            -v /var/run/docker.sock:/var/run/docker.sock \
            airflow_pyspark_spark-app:latest \
            spark-submit --master spark://spark-master:7077 \
            --jars /opt/jars/postgresql-42.7.7.jar /app/app.py
        """
    )

run_spark_job