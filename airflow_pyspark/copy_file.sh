#!/bin/bash

until pg_isready -h postgres -p 5432 -U airflow; do
  sleep 2
done
echo "PostgreSQL is ready. Importing source files."
psql -h postgres -U airflow -d airflow -c "\COPY source_data FROM '/app/merged.csv' WITH (FORMAT csv, HEADER true, DELIMITER ',', NULL '')"