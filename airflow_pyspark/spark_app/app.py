import time
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, count, round, hour, date_format, when, avg
from pyspark.sql.types import TimestampType

jdbc_url = "jdbc:postgresql://postgres:5432/airflow"
properties = {
    "user": "airflow",
    "password": "airflow",
    "driver": "org.postgresql.Driver"
}
source_table_name = "source_data"

spark = SparkSession.builder.appName("DataTransformationSpark").getOrCreate()

for i in range(10):
    try:
        df = spark.read.format("jdbc") \
            .option("url", jdbc_url) \
            .option("dbtable", source_table_name) \
            .option("user", properties["user"]) \
            .option("password", properties["password"]) \
            .option("driver", properties["driver"]) \
            .load()

        if df.take(1):
            print("Data found in source_data. Displaying sample:")
            df.show(10)
            break
        else:
            print(f"Table is still empty. Retrying... [{i + 1}/10]")
            time.sleep(30)

    except Exception as e:
        print(f"Connection or read failed. Retrying... [{i + 1}/10] - {e}")
        time.sleep(5)
else:
    raise RuntimeError("Data not loaded after 10 attempts. Exiting.")

df = df.withColumn("pickup_datetime", col("pickup_datetime").cast(TimestampType())) \
       .withColumn("dropoff_datetime", col("dropoff_datetime").cast(TimestampType()))

total_count = df.count()
platform_counts = (
    df.groupBy("hvfhs_license_num")
      .agg(count("*").alias("trip_count"))
      .withColumn("percentage", round(col("trip_count") / total_count * 100, 2))
      .orderBy(col("trip_count").desc())
)

top_N_location = (
    df.groupBy("PULocationID")
      .agg(count("*").alias("pickup_count"))
      .orderBy(col("pickup_count").desc())
      .limit(10)
)

extract_hour_df = (
    df.withColumn("hour", hour(col("pickup_datetime")))
      .withColumn("weekday", date_format("pickup_datetime", "E"))
)

time_df = (
    extract_hour_df.groupBy("hour")
      .agg(count("*").alias("trip_count"))
      .orderBy("hour")
      .limit(24)
)

date_df = (
    extract_hour_df.groupBy("weekday")
      .agg(count("*").alias("trip_count"))
      .orderBy(col("trip_count").desc())
)

wav_stats = (
    df.select(
        when(col("wav_request_flag") == "Y", 1).otherwise(0).alias("is_wav_requested"),
        when((col("wav_request_flag") == "Y") & (col("dispatching_base_num").isNotNull()), 1).otherwise(0).alias("is_wav_matched")
    ).agg(
        count(when(col("is_wav_requested") == 1, True)).alias("total_requested"),
        count(when(col("is_wav_matched") == 1, True)).alias("total_matched")
    )
)

congestion_fee = (
    df.withColumn("congestion_flag", when(col("congestion_surcharge") > 0, "Yes").otherwise("No"))
      .groupBy("congestion_flag")
      .agg(
          avg("trip_miles").alias("avg_trip_distance"),
          avg("base_passenger_fare").alias("avg_passenger_fare"),
          avg("driver_pay").alias("avg_driver_pay"),
          count("*").alias("num_trips")
      )
)

dataframes_to_save = [
    (platform_counts, "agg_platform_percentage"),
    (top_N_location, "agg_top_pickup_location"),
    (time_df, "agg_hourly_demand"),
    (date_df, "agg_weekday_demand"),
    (wav_stats, "agg_wav_stats"),
    (congestion_fee, "agg_congestion_fee")
]

for df_result, table_name in dataframes_to_save:
    df_result.write \
        .format("jdbc") \
        .option("url", jdbc_url) \
        .option("dbtable", table_name) \
        .option("user", properties["user"]) \
        .option("password", properties["password"]) \
        .option("driver", properties["driver"]) \
        .mode("overwrite") \
        .save()

spark.stop()
