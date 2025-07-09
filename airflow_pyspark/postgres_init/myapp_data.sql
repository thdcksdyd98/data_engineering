CREATE TABLE IF NOT EXISTS source_data (
    id SERIAL PRIMARY KEY,
    name TEXT,
    address TEXT,
    comment TEXT,
    price NUMERIC,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS target_data(
    
);