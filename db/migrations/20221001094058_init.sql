-- migrate:up

CREATE TABLE metrics (
    name TEXT,
    url TEXT,
    response_time FLOAT,
    status_code INT,
    regex TEXT,
    regex_check BOOLEAN,
    timestamp TIMESTAMP
);

-- migrate:down

DROP TABLE metrics;

