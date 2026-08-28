-- =====================================================================
-- BED 106 Business Analytics - Mini Capstone: Sales Trend Analysis
-- Checkpoint 1: SCREENSHOT SCRIPT
--
-- Run these one block at a time in phpMyAdmin or MySQL Workbench and
-- screenshot each result. Blocks S1-S6 fill the Task 1.3 screenshot slots
-- (schema and populated tables); blocks Q1-Q8 fill the Task 1.4 slots.
--
-- BEFORE YOU START, load the database:
--     mysql -u root -p < sql/01_schema_mysql.sql
--     mysql -u root -p sales_trend < sql/03_insert_data.sql
--
-- In phpMyAdmin: select the sales_trend database, open the SQL tab, paste
-- ONE block, press Go, screenshot the query and its result together.
--
-- Every block prints the expected answer in its comment. If your result
-- differs, the load did not work - fix that before screenshotting.
-- =====================================================================

USE sales_trend;


-- =====================================================================
-- PART A - TASK 1.3 SCREENSHOTS (schema and populated tables)
-- =====================================================================

-- ---------------------------------------------------------------------
-- S1. All tables in the database.
--     EXPECT: exactly 8 rows - categories, cities, customers,
--     dates, payment_modes, states, sub_categories, sales
-- ---------------------------------------------------------------------
SHOW TABLES;


-- ---------------------------------------------------------------------
-- S2. Structure of the fact table, showing data types and the primary key.
--     EXPECT: 9 columns; sale_id marked PRI.
--     Repeat for any dimension you also want to show, e.g.
--     DESCRIBE customers;
-- ---------------------------------------------------------------------
DESCRIBE sales;


-- ---------------------------------------------------------------------
-- S3. The full CREATE statement, showing primary keys, foreign keys,
--     CHECK constraints and indexes in one screenshot. This is the single
--     most useful image for the "schema" slot.
--     EXPECT: 4 FOREIGN KEY clauses and 2 CHECK constraints.
-- ---------------------------------------------------------------------
SHOW CREATE TABLE sales;


-- ---------------------------------------------------------------------
-- S4. Every foreign key in the database, listed as parent -> child.
--     Proves the tables are genuinely related, which is what the rubric
--     asks for ("at least 2 related tables").
--     EXPECT: 7 rows.
-- ---------------------------------------------------------------------
SELECT
    kcu.TABLE_NAME                AS child_table,
    kcu.COLUMN_NAME               AS foreign_key_column,
    kcu.REFERENCED_TABLE_NAME     AS parent_table,
    kcu.REFERENCED_COLUMN_NAME    AS parent_key_column,
    kcu.CONSTRAINT_NAME           AS constraint_name
FROM information_schema.KEY_COLUMN_USAGE AS kcu
WHERE kcu.TABLE_SCHEMA = 'sales_trend'
  AND kcu.REFERENCED_TABLE_NAME IS NOT NULL
ORDER BY kcu.REFERENCED_TABLE_NAME, kcu.TABLE_NAME;


-- ---------------------------------------------------------------------
-- S5. Row count of every table in one result - the "populated tables"
--     screenshot.
--     EXPECT, in this order: 3, 18, 807, 648, 5, 6, 12, 1194
-- ---------------------------------------------------------------------
SELECT 'categories'     AS table_name, COUNT(*) AS row_count FROM categories
UNION ALL SELECT 'cities',             COUNT(*) FROM cities
UNION ALL SELECT 'customers',         COUNT(*) FROM customers
UNION ALL SELECT 'dates',             COUNT(*) FROM dates
UNION ALL SELECT 'payment_modes',     COUNT(*) FROM payment_modes
UNION ALL SELECT 'states',            COUNT(*) FROM states
UNION ALL SELECT 'sub_categories',     COUNT(*) FROM sub_categories
UNION ALL SELECT 'sales',           COUNT(*) FROM sales;


-- ---------------------------------------------------------------------
-- S6. Data-integrity proof. Every number here should match the comment;
--     the two orphan counts MUST be 0. Screenshot this to show the load
--     was clean, not just that rows exist.
--     EXPECT: 1194 | 6182639.00 | 547 | 57 | 0 | 0
-- ---------------------------------------------------------------------
SELECT
    (SELECT COUNT(*)  FROM sales)                       AS sales_rows,
    (SELECT SUM(amount) FROM sales)                     AS total_revenue,
    (SELECT COUNT(DISTINCT order_ref) FROM sales)       AS distinct_order_refs,
    (SELECT COUNT(DISTINCT dates.year_month) FROM dates
      WHERE is_complete_year = 1 AND is_complete_month = 1)  AS analysis_months,
    (SELECT COUNT(*) FROM sales f
       LEFT JOIN customers c ON c.customer_id = f.customer_id
      WHERE c.customer_id IS NULL)                           AS orphan_customers,
    (SELECT COUNT(*) FROM sales f
       LEFT JOIN dates d ON d.order_date = f.order_date
      WHERE d.order_date IS NULL)                            AS orphan_dates;


-- ---------------------------------------------------------------------
-- S7 (optional but strong). The raw-data problem that justifies the
--     surrogate key: one Order ID across three dates and three customers.
--     Pair this with the Task 1.2 duplicate discussion.
--     EXPECT: 3 rows, all order_ref = 'B-26776', different dates/customers.
-- ---------------------------------------------------------------------
SELECT
    f.sale_id,
    f.order_ref,
    f.order_date,
    cu.customer_name,
    ci.city_name,
    f.amount
FROM sales   AS f
JOIN customers AS cu ON cu.customer_id = f.customer_id
JOIN cities     AS ci ON ci.city_id     = cu.city_id
WHERE f.order_ref = 'B-26776'
  AND f.sub_category_id = (SELECT sub_category_id FROM sub_categories
                            WHERE sub_category_name = 'Electronic Games')
ORDER BY f.order_date;


-- =====================================================================
-- PART B - TASK 1.4 SCREENSHOTS (the eight queries)
--
-- These are identical to sql/04_queries.sql. Run each on its own and
-- screenshot the SQL and its result set together.
-- =====================================================================

-- ---------------------------------------------------------------------
-- Q1. BASIC RETRIEVAL - the 15 largest transaction lines of 2024.
--     Clauses: SELECT, WHERE, ORDER BY
--     EXPECT: 15 rows, amount from 9,914 down to 9,380.
-- ---------------------------------------------------------------------
SELECT
    sale_id,
    order_ref,
    order_date,
    quantity,
    amount,
    profit
FROM sales
WHERE order_date >= '2024-01-01'
  AND order_date <= '2024-12-31'
ORDER BY amount DESC
LIMIT 15;


-- ---------------------------------------------------------------------
-- Q2. BASIC RETRIEVAL - bulk orders sold at a thin margin.
--     Clauses: SELECT, WHERE, ORDER BY, calculated column
--     EXPECT: 15 rows; the worst is sale_id 8 at 0.78% margin.
-- ---------------------------------------------------------------------
SELECT
    sale_id,
    order_date,
    quantity,
    amount,
    profit,
    ROUND(100.0 * profit / amount, 2) AS margin_pct
FROM sales
WHERE quantity >= 15
  AND profit < 0.15 * amount
-- sale_id breaks ties: three rows share the same margin AND amount, so
-- without it the row order is left to the database engine.
ORDER BY margin_pct ASC, amount DESC, sale_id ASC
LIMIT 15;


-- ---------------------------------------------------------------------
-- Q3. AGGREGATE - annual sales trend, 2020-2024.
--     Clauses: GROUP BY, COUNT, SUM, AVG
--     NOTE: months_covered shows 9 for 2020, because the file starts on
--     22 March 2020. Compare years on revenue_per_month, not revenue.
--     EXPECT: 5 rows; 2022 peaks at 121,647.92 per month.
-- ---------------------------------------------------------------------
SELECT
    d.year_number                                   AS year,
    COUNT(DISTINCT d.year_month)                    AS months_covered,
    COUNT(*)                                        AS transaction_lines,
    SUM(f.quantity)                                 AS units_sold,
    ROUND(SUM(f.amount), 2)                         AS revenue,
    ROUND(SUM(f.profit), 2)                         AS profit,
    ROUND(SUM(f.amount) / COUNT(DISTINCT d.year_month), 2)
                                                    AS revenue_per_month,
    ROUND(AVG(f.amount), 2)                         AS avg_line_value,
    ROUND(100.0 * SUM(f.profit) / SUM(f.amount), 2) AS margin_pct
FROM sales AS f
JOIN dates AS d
      ON d.order_date = f.order_date
WHERE d.is_complete_year = 1
  AND d.is_complete_month = 1
GROUP BY d.year_number
ORDER BY d.year_number;


-- ---------------------------------------------------------------------
-- Q4. AGGREGATE - monthly seasonality with each month's share of the year.
--     Clauses: GROUP BY, COUNT, SUM, AVG, scalar subquery
--     EXPECT: 12 rows; December highest at 11.09%, January lowest at 4.73%.
-- ---------------------------------------------------------------------
SELECT
    d.month_number                  AS month_no,
    d.month_name                    AS month,
    COUNT(*)                        AS transaction_lines,
    ROUND(SUM(f.amount), 2)         AS revenue,
    ROUND(AVG(f.amount), 2)         AS avg_line_value,
    ROUND(
        100.0 * SUM(f.amount) / (
            SELECT SUM(f2.amount)
            FROM sales AS f2
            JOIN dates AS d2 ON d2.order_date = f2.order_date
            WHERE d2.is_complete_year = 1
              AND d2.is_complete_month = 1
        ), 2)                       AS pct_of_total_revenue
FROM sales AS f
JOIN dates AS d
      ON d.order_date = f.order_date
WHERE d.is_complete_year = 1
  AND d.is_complete_month = 1
GROUP BY d.month_number, d.month_name
ORDER BY d.month_number;


-- ---------------------------------------------------------------------
-- Q5. JOIN (4 tables) - revenue by product category per year.
--     sales -> dates, and -> sub_categories -> categories
--     EXPECT: 15 rows; Electronics drops from 538,319 (2023) to 318,630 (2024).
-- ---------------------------------------------------------------------
SELECT
    c.category_name                                 AS category,
    d.year_number                                   AS year,
    COUNT(*)                                        AS transaction_lines,
    ROUND(SUM(f.amount), 2)                         AS revenue,
    ROUND(SUM(f.profit), 2)                         AS profit,
    ROUND(100.0 * SUM(f.profit) / SUM(f.amount), 2) AS margin_pct
FROM sales AS f
JOIN dates         AS d ON d.order_date       = f.order_date
JOIN sub_categories AS s ON s.sub_category_id  = f.sub_category_id
JOIN categories     AS c ON c.category_id      = s.category_id
WHERE d.is_complete_year = 1
GROUP BY c.category_name, d.year_number
ORDER BY c.category_name, d.year_number;


-- ---------------------------------------------------------------------
-- Q6. JOIN (4 tables) - top 10 cities by revenue.
--     sales -> customers -> cities -> states
--     EXPECT: 10 rows; Orlando first at 452,158 and 9,829.52 per customer.
-- ---------------------------------------------------------------------
SELECT
    st.state_name                                   AS state,
    ci.city_name                                    AS city,
    COUNT(DISTINCT cu.customer_id)                  AS customers,
    COUNT(*)                                        AS transaction_lines,
    ROUND(SUM(f.amount), 2)                         AS revenue,
    ROUND(SUM(f.amount) / COUNT(DISTINCT cu.customer_id), 2)
                                                    AS revenue_per_customer,
    ROUND(100.0 * SUM(f.profit) / SUM(f.amount), 2) AS margin_pct
FROM sales   AS f
JOIN customers AS cu ON cu.customer_id = f.customer_id
JOIN cities     AS ci ON ci.city_id     = cu.city_id
JOIN states    AS st ON st.state_id    = ci.state_id
GROUP BY st.state_name, ci.city_name
ORDER BY revenue DESC
LIMIT 10;


-- ---------------------------------------------------------------------
-- Q7. BUSINESS INSIGHT - which sub-categories caused the plateau?
--     Answers key business question 2. Conditional aggregation.
--     EXPECT: 12 rows; Printers worst at -136,865 (-71.0%),
--     Paper best at +85,689 (+149.4%).
-- ---------------------------------------------------------------------
SELECT
    c.category_name AS category,
    s.sub_category_name AS sub_category,
    ROUND(SUM(CASE WHEN d.year_number = 2023 THEN f.amount ELSE 0 END), 2)
        AS revenue_2023,
    ROUND(SUM(CASE WHEN d.year_number = 2024 THEN f.amount ELSE 0 END), 2)
        AS revenue_2024,
    ROUND(SUM(CASE WHEN d.year_number = 2024 THEN f.amount ELSE 0 END)
        - SUM(CASE WHEN d.year_number = 2023 THEN f.amount ELSE 0 END), 2)
        AS change_abs,
    ROUND(100.0 *
        (SUM(CASE WHEN d.year_number = 2024 THEN f.amount ELSE 0 END)
       - SUM(CASE WHEN d.year_number = 2023 THEN f.amount ELSE 0 END))
        / NULLIF(SUM(CASE WHEN d.year_number = 2023 THEN f.amount ELSE 0 END), 0), 1)
        AS change_pct
FROM sales       AS f
JOIN dates         AS d ON d.order_date      = f.order_date
JOIN sub_categories AS s ON s.sub_category_id = f.sub_category_id
JOIN categories     AS c ON c.category_id     = s.category_id
WHERE d.year_number IN (2023, 2024)
GROUP BY c.category_name, s.sub_category_name
ORDER BY change_abs ASC;


-- ---------------------------------------------------------------------
-- Q8. BUSINESS INSIGHT - is the Q4 peak company-wide or category-specific?
--     Answers key business question 3. Window function.
--     NOTE: needs MySQL 8.0 or later. If your server is MySQL 5.7, use
--     the alternative immediately below instead.
--     EXPECT: 12 rows; Electronics peaks in Q2 (30.79%), Furniture and
--     Office Supplies peak in Q4 (30.84% and 32.16%).
-- ---------------------------------------------------------------------
SELECT
    c.category_name         AS category,
    d.quarter_number        AS quarter,
    COUNT(*)                AS transaction_lines,
    ROUND(SUM(f.amount), 2) AS revenue,
    ROUND(100.0 * SUM(f.amount) / SUM(SUM(f.amount)) OVER (
              PARTITION BY c.category_name), 2)
                            AS pct_of_category_revenue
FROM sales       AS f
JOIN dates         AS d ON d.order_date      = f.order_date
JOIN sub_categories AS s ON s.sub_category_id = f.sub_category_id
JOIN categories     AS c ON c.category_id     = s.category_id
WHERE d.is_complete_year = 1
  AND d.is_complete_month = 1
GROUP BY c.category_name, d.quarter_number
ORDER BY c.category_name, d.quarter_number;


-- ---------------------------------------------------------------------
-- Q8-ALT. Same result without a window function, for MySQL 5.7 and
--     older phpMyAdmin installations. Uses a correlated subquery for the
--     category total instead of OVER (PARTITION BY ...).
--     Produces identical numbers to Q8.
-- ---------------------------------------------------------------------
SELECT
    c.category_name         AS category,
    d.quarter_number        AS quarter,
    COUNT(*)                AS transaction_lines,
    ROUND(SUM(f.amount), 2) AS revenue,
    ROUND(100.0 * SUM(f.amount) / (
        SELECT SUM(f2.amount)
        FROM sales       AS f2
        JOIN dates         AS d2 ON d2.order_date      = f2.order_date
        JOIN sub_categories AS s2 ON s2.sub_category_id = f2.sub_category_id
        WHERE s2.category_id = c.category_id
          AND d2.is_complete_year = 1
          AND d2.is_complete_month = 1
    ), 2)                   AS pct_of_category_revenue
FROM sales       AS f
JOIN dates         AS d ON d.order_date      = f.order_date
JOIN sub_categories AS s ON s.sub_category_id = f.sub_category_id
JOIN categories     AS c ON c.category_id     = s.category_id
WHERE d.is_complete_year = 1
  AND d.is_complete_month = 1
GROUP BY c.category_name, c.category_id, d.quarter_number
ORDER BY c.category_name, d.quarter_number;
