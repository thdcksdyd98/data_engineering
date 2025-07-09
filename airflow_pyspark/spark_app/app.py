import time
from pyspark.sql import SparkSession

jdbc_url = "jdbc:postgresql://postgresql:5432/psql_db"
properties = {
    "user": "admin",
    "password": "admin",
    "driver": "org.postgresql.Driver"
}
source_table_name = "source_data"
target_table_name = "target_data"

for i in range(10):
    try:
        spark = SparkSession.builder.appName("DataTransformationSpark").getOrCreate()
        source_df = spark.read.jdbc(url=jdbc_url, table=source_table_name, properties=properties)
        break
    except Exception as e:
        print(f"Connection Failed. Retrying... [{i+1}/10]")
        time.sleep(5)
else:
    raise RuntimeError("Connection Failed. Shutting Down...")

