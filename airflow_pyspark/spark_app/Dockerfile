FROM apache/spark:3.4.1

USER root

RUN apt-get update && apt-get install -y procps curl python3 python3-pip
RUN pip3 install pyspark psycopg2-binary pandas

COPY jars/postgresql-42.7.7.jar /opt/jars/
COPY app.py /app/app.py

WORKDIR /app

