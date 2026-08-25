-- =====================================================================
-- BED 106 Business Analytics - Mini Capstone: Sales Trend Analysis
-- Checkpoint 1, Task 1.3: Relational Database Design
--
-- Target RDBMS: MySQL 8.0
-- Design      : star schema - one fact table (fact_sales) surrounded by
--               six conformed dimensions. Chosen because every key
--               business question in Task 1.1 is "a measure, sliced by a
--               dimension, over time", which is exactly what this shape
--               answers in a single join hop.
--
-- Run order:   01_schema_mysql.sql -> 03_insert_data.sql -> 04_queries.sql
-- =====================================================================

DROP DATABASE IF EXISTS sales_trend;
CREATE DATABASE sales_trend
    DEFAULT CHARACTER SET utf8mb4
    DEFAULT COLLATE utf8mb4_unicode_ci;
USE sales_trend;

-- ---------------------------------------------------------------------
-- Geography: state 1---* city 1---* customer
-- ---------------------------------------------------------------------
CREATE TABLE dim_state (
    state_id    INT           NOT NULL,
    state_name  VARCHAR(60)   NOT NULL,
    CONSTRAINT pk_dim_state PRIMARY KEY (state_id),
    CONSTRAINT uq_dim_state_name UNIQUE (state_name)
) ENGINE = InnoDB;

CREATE TABLE dim_city (
    city_id     INT           NOT NULL,
    city_name   VARCHAR(60)   NOT NULL,
    state_id    INT           NOT NULL,
    CONSTRAINT pk_dim_city PRIMARY KEY (city_id),
    -- A city name is only unique inside its state.
    CONSTRAINT uq_dim_city UNIQUE (city_name, state_id),
    CONSTRAINT fk_city_state FOREIGN KEY (state_id)
        REFERENCES dim_state (state_id)
) ENGINE = InnoDB;

CREATE TABLE dim_customer (
    customer_id   INT          NOT NULL,
    customer_name VARCHAR(120) NOT NULL,
    city_id       INT          NOT NULL,
    CONSTRAINT pk_dim_customer PRIMARY KEY (customer_id),
    -- CustomerName alone repeats across cities in the raw file, so the
    -- business key is the (name, city) pair.
    CONSTRAINT uq_dim_customer UNIQUE (customer_name, city_id),
    CONSTRAINT fk_customer_city FOREIGN KEY (city_id)
        REFERENCES dim_city (city_id)
) ENGINE = InnoDB;

-- ---------------------------------------------------------------------
-- Product hierarchy: category 1---* sub_category
-- ---------------------------------------------------------------------
CREATE TABLE dim_category (
    category_id   INT         NOT NULL,
    category_name VARCHAR(60) NOT NULL,
    CONSTRAINT pk_dim_category PRIMARY KEY (category_id),
    CONSTRAINT uq_dim_category_name UNIQUE (category_name)
) ENGINE = InnoDB;

CREATE TABLE dim_sub_category (
    sub_category_id   INT         NOT NULL,
    sub_category_name VARCHAR(60) NOT NULL,
    category_id       INT         NOT NULL,
    CONSTRAINT pk_dim_sub_category PRIMARY KEY (sub_category_id),
    CONSTRAINT uq_dim_sub_category UNIQUE (sub_category_name, category_id),
    CONSTRAINT fk_sub_category_category FOREIGN KEY (category_id)
        REFERENCES dim_category (category_id)
) ENGINE = InnoDB;

-- ---------------------------------------------------------------------
-- Payment method
-- ---------------------------------------------------------------------
CREATE TABLE dim_payment_mode (
    payment_mode_id   INT         NOT NULL,
    payment_mode_name VARCHAR(40) NOT NULL,
    CONSTRAINT pk_dim_payment_mode PRIMARY KEY (payment_mode_id),
    CONSTRAINT uq_dim_payment_mode_name UNIQUE (payment_mode_name)
) ENGINE = InnoDB;

-- ---------------------------------------------------------------------
-- Calendar. Pre-computing the parts of the date keeps the trend queries
-- readable and lets is_complete_year fence off the partial 2025 window.
-- ---------------------------------------------------------------------
CREATE TABLE dim_date (
    order_date       DATE        NOT NULL,
    year_number      SMALLINT    NOT NULL,
    quarter_number   TINYINT     NOT NULL,
    month_number     TINYINT     NOT NULL,
    month_name       VARCHAR(12) NOT NULL,
    year_month       CHAR(7)     NOT NULL,
    is_complete_year TINYINT     NOT NULL,
    CONSTRAINT pk_dim_date PRIMARY KEY (order_date),
    CONSTRAINT ck_dim_date_quarter CHECK (quarter_number BETWEEN 1 AND 4),
    CONSTRAINT ck_dim_date_month   CHECK (month_number BETWEEN 1 AND 12)
) ENGINE = InnoDB;

-- ---------------------------------------------------------------------
-- Fact table. Grain: one row per transaction line.
-- order_ref keeps the raw "Order ID" for traceability but is NOT a key -
-- the raw values are reused across dates and customers.
-- ---------------------------------------------------------------------
CREATE TABLE fact_sales (
    sale_id         INT      NOT NULL,
    order_ref       VARCHAR(20) NOT NULL,
    order_date      DATE     NOT NULL,
    customer_id     INT      NOT NULL,
    sub_category_id INT      NOT NULL,
    payment_mode_id INT      NOT NULL,
    quantity        INT      NOT NULL,
    amount          DECIMAL(12, 2) NOT NULL,
    profit          DECIMAL(12, 2) NOT NULL,
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
) ENGINE = InnoDB;

-- Indexes on the columns the Task 1.4 queries filter and group by.
CREATE INDEX ix_fact_sales_date         ON fact_sales (order_date);
CREATE INDEX ix_fact_sales_sub_category ON fact_sales (sub_category_id);
CREATE INDEX ix_fact_sales_customer     ON fact_sales (customer_id);
CREATE INDEX ix_fact_sales_payment      ON fact_sales (payment_mode_id);
