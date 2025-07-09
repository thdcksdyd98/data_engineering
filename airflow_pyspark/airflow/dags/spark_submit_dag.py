from airflow import DAG
from airflow.providers.docker.operators.docker import DockerOperator
from datetime import datetime, timedelta

default_args={
    'owner':'airflow',
    'start_date':datetime.today() - timedelta(days=1),
    'retries':3
}
with DAG(
    dag_id='spark_dag',
    default_args=default_args,
    schedule_interval='@daily',
    catchup=False
) as dag:
    run_spark_job=DockerOperator(
        task_id='run_spark_app',
        image='airflow_pyspark-spark-app:latest',
        api_version='atuo',
        auto_remove=True,
        command="spark-submit --master spark://spark-master:7077 --jars /opt/jars/postgresql-42.7.7.jar /app/app.py",
        docker_url='unix://var/run/docker.sock',
        network_mode='airflow_pyspark_mynet',
        mount_tmp_dir=False
    )