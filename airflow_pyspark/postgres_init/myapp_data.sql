CREATE DATABASE myapp_data;

CREATE TABLE IF NOT EXISTS mock_data (
    id SERIAL PRIMARY KEY,
    name TEXT,
    address TEXT,
    comment TEXT,
    price NUMERIC,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);