```

data_engineering
├── airflow_pyspark
│   ├── airflow
│   │   └── dags
│   │       └── spark_submit_dag.py
│   ├── docker-compose.yml
│   ├── init_script.py
│   ├── postgres_init
│   │   └── myapp_data.sql
│   ├── README.md
│   └── spark_app
│       ├── app.py
│       ├── Dockerfile
│       └── jars
│           └── postgresql-42.7.7.jar
└── README.md


        [ HOST MACHINE ]
   ┌────────────────────────┐
   │                        │
   │  http://localhost:8080 │ → Airflow UI
   │  http://localhost:8081 │ → Spark Master UI
   │                        │
   └────────────┬───────────┘
                │
  Host-to-container port mapping
                ▼
==========================================================
DOCKER BRIDGE NETWORK  (Shared internal container network)        
==========================================================
• All containers are on the same internal Docker network
• They communicate using internal ports and service names (DNS)
• No need for host ports when containers talk to each other
• Defined automatically by docker-compose

┌────────────────────────────────────────────────────┐
│     airflow (service: airflow)                     │
│     - Internal Port: 8080                          │
│     - Exposed as: localhost:8080                   │
│     - Triggers spark-app using DockerOperator      │
└───────────────┬────────────────────────────────────┘
                │
                │ triggers
                ▼
┌────────────────────────────────────────────────────┐
│     spark-app (service: spark-app)                 │
│     - No exposed port                              │
│     - Runs PySpark script                          │
│     - Uses master URL: spark://spark-master:7077   │
│     - Reads/Writes via JDBC to postgres:5432       │
└───────────────┬────────────────────────────────────┘
                │
                │ connects to Spark master
                ▼
┌────────────────────────────────────────────────────┐
│     spark-master (service: spark-master)           │
│     - Internal Port: 7077 (RPC)                    │
│     - Internal Port: 8080 → Host: 8081 (Web UI)    │
│     - Distributes jobs to workers                  │
└───────────────┬────────────────────────────────────┘
                │
                │ auto connects
                ▼
┌────────────────────────────────────────────────────┐
│     spark-worker (service: spark-worker)           │
│     - Auto-registered with spark-master:7077       │
└────────────────────────────────────────────────────┘
                ▲
                │
┌───────────────┴────────────────────────────────────┐
│     postgres (service: postgres)                   │
│     - Internal Port: 5432                          │
│     - Exposed as: localhost:5432 (optional)        │
│     - Accessed by spark-app via:                   │
│         jdbc:postgresql://postgres:5432/testdb     │
└────────────────────────────────────────────────────┘
 

docker compose down -v --remove-orphans -> remove all container, network, and volumes

```