FROM python:3.9-slim

# Java 설치
RUN apt-get update && \
    apt-get install -y --no-install-recommends openjdk-17-jdk ca-certificates && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# pyspark 호환을 위한 심볼릭 링크
RUN ln -s /usr/lib/jvm/java-17-openjdk-arm64 /usr/lib/jvm/java-17-openjdk-amd64

# JAVA_HOME 설정 (pyspark와 일치)
ENV JAVA_HOME=/usr/lib/jvm/java-17-openjdk-amd64
ENV PATH=$JAVA_HOME/bin:$PATH

# 나머지 PySpark 설치 및 복사
RUN pip install pyspark==3.4.1
COPY jars/postgresql-42.7.7.jar /opt/jars/postgresql-42.7.7.jar
COPY app.py /app/app.py
WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends bash && rm -rf /var/lib/apt/lists/*

ENTRYPOINT ["bash", "-c"]
CMD ["spark-submit --master spark://spark-master:7077 --jars /opt/jars/postgresql-42.7.7.jar app.py"]
