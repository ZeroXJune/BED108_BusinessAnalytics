-- =====================================================================
-- BED 106 Business Analytics - Mini Capstone: Sales Trend Analysis
-- Checkpoint 1, Task 1.3: Relational Database Design
--
-- Target RDBMS: MySQL 8.0
-- Design      : star schema - one fact table (sales) surrounded by
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
CREATE TABLE states (
    state_id    INT           NOT NULL,
    state_name  VARCHAR(60)   NOT NULL,
    CONSTRAINT pk_states PRIMARY KEY (state_id),
    CONSTRAINT uq_states_name UNIQUE (state_name)
) ENGINE = InnoDB;

CREATE TABLE cities (
    city_id     INT           NOT NULL,
    city_name   VARCHAR(60)   NOT NULL,
    state_id    INT           NOT NULL,
    CONSTRAINT pk_cities PRIMARY KEY (city_id),
    -- A city name is only unique inside its state.
    CONSTRAINT uq_cities UNIQUE (city_name, state_id),
    CONSTRAINT fk_cities_states FOREIGN KEY (state_id)
        REFERENCES states (state_id)
) ENGINE = InnoDB;

CREATE TABLE customers (
    customer_id   INT          NOT NULL,
    customer_name VARCHAR(120) NOT NULL,
    city_id       INT          NOT NULL,
    CONSTRAINT pk_customers PRIMARY KEY (customer_id),
    -- CustomerName alone repeats across cities in the raw file, so the
    -- business key is the (name, city) pair.
    CONSTRAINT uq_customers UNIQUE (customer_name, city_id),
    CONSTRAINT fk_customers_cities FOREIGN KEY (city_id)
        REFERENCES cities (city_id)
) ENGINE = InnoDB;

-- ---------------------------------------------------------------------
-- Product hierarchy: category 1---* sub_category
-- ---------------------------------------------------------------------
CREATE TABLE categories (
    category_id   INT         NOT NULL,
    category_name VARCHAR(60) NOT NULL,
    CONSTRAINT pk_categories PRIMARY KEY (category_id),
    CONSTRAINT uq_categories_name UNIQUE (category_name)
) ENGINE = InnoDB;

CREATE TABLE sub_categories (
    sub_category_id   INT         NOT NULL,
    sub_category_name VARCHAR(60) NOT NULL,
    category_id       INT         NOT NULL,
    CONSTRAINT pk_sub_categories PRIMARY KEY (sub_category_id),
    CONSTRAINT uq_sub_categories UNIQUE (sub_category_name, category_id),
    CONSTRAINT fk_sub_categories_categories FOREIGN KEY (category_id)
        REFERENCES categories (category_id)
) ENGINE = InnoDB;

-- ---------------------------------------------------------------------
-- Payment method
-- ---------------------------------------------------------------------
CREATE TABLE payment_modes (
    payment_mode_id   INT         NOT NULL,
    payment_mode_name VARCHAR(40) NOT NULL,
    CONSTRAINT pk_payment_modes PRIMARY KEY (payment_mode_id),
    CONSTRAINT uq_payment_modes_name UNIQUE (payment_mode_name)
) ENGINE = InnoDB;

-- ---------------------------------------------------------------------
-- Calendar. Pre-computing the parts of the date keeps the trend queries
-- readable and lets the two flags fence off partial windows:
--   is_complete_year  - 2025 stops on 15 March, so it is not a full year.
--   is_complete_month - the file also STARTS on 22 March 2020, so both the
--                       first and last calendar months are partial. A partial
--                       month is not a valid monthly observation.
--
-- NOTE: `year_month` is backticked because YEAR_MONTH is a reserved word in
-- MySQL and MariaDB (the INTERVAL ... YEAR_MONTH unit). Unqualified and
-- unquoted it is a syntax error; write dates.year_month or `year_month`.
-- ---------------------------------------------------------------------
CREATE TABLE dates (
    order_date       DATE        NOT NULL,
    year_number      SMALLINT    NOT NULL,
    quarter_number   TINYINT     NOT NULL,
    month_number     TINYINT     NOT NULL,
    month_name       VARCHAR(12) NOT NULL,
    `year_month`     CHAR(7)     NOT NULL,
    is_complete_year TINYINT     NOT NULL,
    is_complete_month TINYINT    NOT NULL,
    CONSTRAINT pk_dates PRIMARY KEY (order_date),
    CONSTRAINT ck_dates_quarter CHECK (quarter_number BETWEEN 1 AND 4),
    CONSTRAINT ck_dates_month   CHECK (month_number BETWEEN 1 AND 12)
) ENGINE = InnoDB;

-- ---------------------------------------------------------------------
-- Fact table. Grain: one row per transaction line.
-- order_ref keeps the raw "Order ID" for traceability but is NOT a key -
-- the raw values are reused across dates and customers.
-- ---------------------------------------------------------------------
CREATE TABLE sales (
    sale_id         INT      NOT NULL,
    order_ref       VARCHAR(20) NOT NULL,
    order_date      DATE     NOT NULL,
    customer_id     INT      NOT NULL,
    sub_category_id INT      NOT NULL,
    payment_mode_id INT      NOT NULL,
    quantity        INT      NOT NULL,
    amount          DECIMAL(12, 2) NOT NULL,
    profit          DECIMAL(12, 2) NOT NULL,
    CONSTRAINT pk_sales PRIMARY KEY (sale_id),
    CONSTRAINT fk_sales_date FOREIGN KEY (order_date)
        REFERENCES dates (order_date),
    CONSTRAINT fk_sales_customer FOREIGN KEY (customer_id)
        REFERENCES customers (customer_id),
    CONSTRAINT fk_sales_sub_category FOREIGN KEY (sub_category_id)
        REFERENCES sub_categories (sub_category_id),
    CONSTRAINT fk_sales_payment_mode FOREIGN KEY (payment_mode_id)
        REFERENCES payment_modes (payment_mode_id),
    CONSTRAINT ck_sales_quantity CHECK (quantity > 0),
    CONSTRAINT ck_sales_amount   CHECK (amount >= 0)
) ENGINE = InnoDB;

-- Indexes on the columns the Task 1.4 queries filter and group by.
CREATE INDEX ix_sales_date         ON sales (order_date);
CREATE INDEX ix_sales_sub_category ON sales (sub_category_id);
CREATE INDEX ix_sales_customer     ON sales (customer_id);
CREATE INDEX ix_sales_payment      ON sales (payment_mode_id);
