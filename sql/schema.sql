-- Create read-only user
CREATE ROLE readonly_user
WITH
    LOGIN PASSWORD 'secure_password' NOSUPERUSER INHERIT NOCREATEDB NOCREATEROLE NOREPLICATION;

GRANT CONNECT ON DATABASE yugabyte TO readonly_user;

ALTER DEFAULT PRIVILEGES IN SCHEMA public
GRANT
SELECT
    ON TABLES TO readonly_user;

GRANT USAGE ON SCHEMA public TO readonly_user;

GRANT
SELECT
    ON ALL TABLES IN SCHEMA public TO readonly_user;

-- pg_trgm uses similarity of alphanumeric text based on trigram matching
CREATE EXTENSION IF NOT EXISTS pg_trgm;

SET
    pg_trgm.similarity_threshold = 0.6;

-- Creating ENUM types for color and width
CREATE TYPE shoe_color AS ENUM(
    'red',
    'green',
    'blue',
    'black',
    'white',
    'yellow',
    'orange',
    'purple',
    'grey',
    'pink'
);

CREATE TYPE shoe_width AS ENUM('narrow', 'medium', 'wide');

CREATE TABLE
    products (
        product_id SERIAL PRIMARY KEY,
        name VARCHAR(255) NOT NULL,
        price DECIMAL(10, 2) NOT NULL,
        color shoe_color[],
        width shoe_width[]
    );

CREATE TABLE
    users (
        user_id SERIAL PRIMARY KEY,
        username VARCHAR(255) UNIQUE NOT NULL,
        email VARCHAR(255) UNIQUE NOT NULL
    );

CREATE TABLE
    purchases (
        purchase_id SERIAL PRIMARY KEY,
        user_id INT REFERENCES users (user_id),
        product_id INT REFERENCES products (product_id),
        purchase_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        quantity INT NOT NULL,
        total_price DECIMAL(10, 2) NOT NULL
    );

CREATE TABLE
    product_inventory (
        inventory_id SERIAL PRIMARY KEY,
        product_id INT REFERENCES products (product_id),
        size INT NOT NULL,
        color shoe_color,
        width shoe_width,
        quantity INT NOT NULL,
        CHECK (quantity >= 0)
    );