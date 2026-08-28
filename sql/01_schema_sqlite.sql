-- =====================================================================
-- BED 106 Business Analytics - Mini Capstone: Sales Trend Analysis
-- Checkpoint 1, Task 1.3: Relational Database Design
--
-- Target RDBMS: SQLite 3 (mirror of 01_schema_mysql.sql, generated for the
--               reproducible local run in scripts/clean_and_load.py)
-- Design      : star schema - one fact table (fact_sales) surrounded by
--               six conformed dimensions. Chosen because every key
--               business question in Task 1.1 is "a measure, sliced by a
--               dimension, over time", which is exactly what this shape
--               answers in a single join hop.
--
-- Run order:   01_schema_mysql.sql -> 03_insert_data.sql -> 04_queries.sql
-- =====================================================================


-- ---------------------------------------------------------------------
-- Geography: state 1---* city 1---* customer
-- ---------------------------------------------------------------------
CREATE TABLE dim_state (
    state_id    INTEGER           NOT NULL,
    state_name  TEXT   NOT NULL,
    CONSTRAINT pk_dim_state PRIMARY KEY (state_id),
    CONSTRAINT uq_dim_state_name UNIQUE (state_name)
);

CREATE TABLE dim_city (
    city_id     INTEGER           NOT NULL,
    city_name   TEXT   NOT NULL,
    state_id    INTEGER           NOT NULL,
    CONSTRAINT pk_dim_city PRIMARY KEY (city_id),
    -- A city name is only unique inside its state.
    CONSTRAINT uq_dim_city UNIQUE (city_name, state_id),
    CONSTRAINT fk_city_state FOREIGN KEY (state_id)
        REFERENCES dim_state (state_id)
);

CREATE TABLE dim_customer (
    customer_id   INTEGER          NOT NULL,
    customer_name TEXT NOT NULL,
    city_id       INTEGER          NOT NULL,
    CONSTRAINT pk_dim_customer PRIMARY KEY (customer_id),
    -- CustomerName alone repeats across cities in the raw file, so the
    -- business key is the (name, city) pair.
    CONSTRAINT uq_dim_customer UNIQUE (customer_name, city_id),
    CONSTRAINT fk_customer_city FOREIGN KEY (city_id)
        REFERENCES dim_city (city_id)
);

-- ---------------------------------------------------------------------
-- Product hierarchy: category 1---* sub_category
-- ---------------------------------------------------------------------
CREATE TABLE dim_category (
    category_id   INTEGER         NOT NULL,
    category_name TEXT NOT NULL,
    CONSTRAINT pk_dim_category PRIMARY KEY (category_id),
    CONSTRAINT uq_dim_category_name UNIQUE (category_name)
);

CREATE TABLE dim_sub_category (
    sub_category_id   INTEGER         NOT NULL,
    sub_category_name TEXT NOT NULL,
    category_id       INTEGER         NOT NULL,
    CONSTRAINT pk_dim_sub_category PRIMARY KEY (sub_category_id),
    CONSTRAINT uq_dim_sub_category UNIQUE (sub_category_name, category_id),
    CONSTRAINT fk_sub_category_category FOREIGN KEY (category_id)
        REFERENCES dim_category (category_id)
);

-- ---------------------------------------------------------------------
-- Payment method
-- ---------------------------------------------------------------------
CREATE TABLE dim_payment_mode (
    payment_mode_id   INTEGER         NOT NULL,
    payment_mode_name TEXT NOT NULL,
    CONSTRAINT pk_dim_payment_mode PRIMARY KEY (payment_mode_id),
    CONSTRAINT uq_dim_payment_mode_name UNIQUE (payment_mode_name)
);

-- ---------------------------------------------------------------------
-- Calendar. Pre-computing the parts of the date keeps the trend queries
-- readable and lets the two flags fence off partial windows:
--   is_complete_year  - 2025 stops on 15 March, so it is not a full year.
--   is_complete_month - the file also STARTS on 22 March 2020, so both the
--                       first and last calendar months are partial. A partial
--                       month is not a valid monthly observation.
-- ---------------------------------------------------------------------
CREATE TABLE dim_date (
    order_date       TEXT        NOT NULL,
    year_number      INTEGER    NOT NULL,
    quarter_number   INTEGER     NOT NULL,
    month_number     INTEGER     NOT NULL,
    month_name       TEXT NOT NULL,
    year_month       TEXT     NOT NULL,
    is_complete_year INTEGER     NOT NULL,
    is_complete_month INTEGER    NOT NULL,
    CONSTRAINT pk_dim_date PRIMARY KEY (order_date),
    CONSTRAINT ck_dim_date_quarter CHECK (quarter_number BETWEEN 1 AND 4),
    CONSTRAINT ck_dim_date_month   CHECK (month_number BETWEEN 1 AND 12)
);

-- ---------------------------------------------------------------------
-- Fact table. Grain: one row per transaction line.
-- order_ref keeps the raw "Order ID" for traceability but is NOT a key -
-- the raw values are reused across dates and customers.
-- ---------------------------------------------------------------------
CREATE TABLE fact_sales (
    sale_id         INTEGER      NOT NULL,
    order_ref       TEXT NOT NULL,
    order_date      TEXT     NOT NULL,
    customer_id     INTEGER      NOT NULL,
    sub_category_id INTEGER      NOT NULL,
    payment_mode_id INTEGER      NOT NULL,
    quantity        INTEGER      NOT NULL,
    amount          REAL NOT NULL,
    profit          REAL NOT NULL,
    CONSTRAINT pk_fact_sales PRIMARY KEY (sale_id),
    CONSTRAINT fk_sales_date FOREIGN KEY (order_date)
        REFERENCES dim_date (order_date),
    CONSTRAINT fk_sales_customer FOREIGN KEY (customer_id)
        REFERENCES dim_customer (customer_id),
    CONSTRAINT fk_sales_sub_category FOREIGN KEY (sub_category_id)
        REFERENCES dim_sub_category (sub_category_id),
    CONSTRAINT fk_sales_payment_mode FOREIGN KEY (payment_mode_id)
        REFERENCES dim_payment_mode (payment_mode_id),
    CONSTRAINT ck_fact_quantity CHECK (quantity > 0),
    CONSTRAINT ck_fact_amount   CHECK (amount >= 0)
);

-- Indexes on the columns the Task 1.4 queries filter and group by.
CREATE INDEX ix_fact_sales_date         ON fact_sales (order_date);
CREATE INDEX ix_fact_sales_sub_category ON fact_sales (sub_category_id);
CREATE INDEX ix_fact_sales_customer     ON fact_sales (customer_id);
CREATE INDEX ix_fact_sales_payment      ON fact_sales (payment_mode_id);
