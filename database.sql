DROP TABLE urls;

DROP TABLE url_check;

CREATE TABLE urls (
    id BIGINT PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    name VARCHAR(255),
    created_at DATE
);

CREATE TABLE url_check (
    id BIGINT PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    url_id BIGINT REFERENCES urls(id),
    status_code INT,
    h1 VARCHAR(255),
    title VARCHAR(255),
    description TEXT,
    created_at DATE
);
