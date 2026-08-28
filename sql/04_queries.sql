-- =====================================================================
-- BED 106 Business Analytics - Mini Capstone: Sales Trend Analysis
-- Checkpoint 1, Task 1.4: SQL Query Report
--
-- Eight queries in four groups:
--   1. Basic data retrieval  (Q1, Q2)  - SELECT / WHERE / ORDER BY
--   2. Aggregate analysis    (Q3, Q4)  - GROUP BY + aggregate functions
--   3. Multi-table joins     (Q5, Q6)  - four tables each
--   4. Business insights     (Q7, Q8)  - answer the Task 1.1 questions
--
-- Every query is written in portable SQL (no dialect-specific date
-- functions) so it runs unchanged on MySQL 8 and SQLite 3. Calendar parts
-- come from dim_date rather than YEAR()/strftime() for that reason.
--
-- The file covers 22 March 2020 to 15 March 2025, so BOTH ends are partial:
--   is_complete_year  = 0 for 2025, which stops on 15 March.
--   is_complete_month = 0 for March 2020 and March 2025, the two part-months.
-- Trend queries filter on these flags so a file cut-off is never misread as
-- a change in demand, and so a 10-day month never sits in a monthly average.
-- =====================================================================


-- =====================================================================
-- 1. BASIC DATA RETRIEVAL
-- =====================================================================

-- ---------------------------------------------------------------------
-- Q1. The 15 largest transaction lines of the most recent complete year.
--     Shows what a "big ticket" looks like in 2024 and which of them
--     were actually profitable.
-- Clauses: SELECT, WHERE, ORDER BY
-- ---------------------------------------------------------------------
SELECT
    sale_id,
    order_ref,
    order_date,
    quantity,
    amount,
    profit
FROM fact_sales
WHERE order_date >= '2024-01-01'
  AND order_date <= '2024-12-31'
ORDER BY amount DESC
LIMIT 15;


-- ---------------------------------------------------------------------
-- Q2. Bulk orders (15+ units) that returned a thin margin. These are the
--     lines where the company moved the most stock for the least return,
--     so they are the first candidates for a pricing or discount review.
-- Clauses: SELECT, WHERE, ORDER BY
-- ---------------------------------------------------------------------
SELECT
    sale_id,
    order_date,
    quantity,
    amount,
    profit,
    ROUND(100.0 * profit / amount, 2) AS margin_pct
FROM fact_sales
WHERE quantity >= 15
  AND profit < 0.15 * amount
ORDER BY margin_pct ASC, amount DESC
LIMIT 15;


-- =====================================================================
-- 2. AGGREGATE ANALYSIS
-- =====================================================================

-- ---------------------------------------------------------------------
-- Q3. Annual sales trend, 2020-2024. The headline table for the whole
--     project: order volume, revenue, profit, average order value and
--     margin for each year.
--
--     IMPORTANT: the file starts on 22 March 2020, so 2020 is a SHORT year.
--     Comparing its annual total against a full 12-month year overstates
--     growth. This query therefore restricts to complete calendar months
--     (is_complete_month = 1) and reports months_covered and
--     revenue_per_month, so every comparison is like for like.
-- Clauses: GROUP BY, COUNT, SUM, AVG
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
FROM fact_sales AS f
JOIN dim_date AS d
      ON d.order_date = f.order_date
WHERE d.is_complete_year = 1
  AND d.is_complete_month = 1
GROUP BY d.year_number
ORDER BY d.year_number;


-- ---------------------------------------------------------------------
-- Q4. Seasonality: revenue by calendar month pooled across the five
--     complete years, with each month's share of the annual total. Tells
--     the team when to hold stock and staff.
-- Clauses: GROUP BY, COUNT, SUM, AVG
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
            FROM fact_sales AS f2
            JOIN dim_date AS d2 ON d2.order_date = f2.order_date
            WHERE d2.is_complete_year = 1
              AND d2.is_complete_month = 1
        ), 2)                       AS pct_of_total_revenue
FROM fact_sales AS f
JOIN dim_date AS d
      ON d.order_date = f.order_date
WHERE d.is_complete_year = 1
  AND d.is_complete_month = 1
GROUP BY d.month_number, d.month_name
ORDER BY d.month_number;


-- =====================================================================
-- 3. MULTI-TABLE JOINS
-- =====================================================================

-- ---------------------------------------------------------------------
-- Q5. Revenue by product category per year.
--     Joins 4 tables: fact_sales -> dim_date
--                                -> dim_sub_category -> dim_category
-- ---------------------------------------------------------------------
SELECT
    c.category_name                                 AS category,
    d.year_number                                   AS year,
    COUNT(*)                                        AS transaction_lines,
    ROUND(SUM(f.amount), 2)                         AS revenue,
    ROUND(SUM(f.profit), 2)                         AS profit,
    ROUND(100.0 * SUM(f.profit) / SUM(f.amount), 2) AS margin_pct
FROM fact_sales AS f
JOIN dim_date         AS d ON d.order_date       = f.order_date
JOIN dim_sub_category AS s ON s.sub_category_id  = f.sub_category_id
JOIN dim_category     AS c ON c.category_id      = s.category_id
WHERE d.is_complete_year = 1
GROUP BY c.category_name, d.year_number
ORDER BY c.category_name, d.year_number;


-- ---------------------------------------------------------------------
-- Q6. Top 10 cities by revenue, with the state they belong to and how
--     many distinct customers each one represents.
--     Joins 4 tables: fact_sales -> dim_customer -> dim_city -> dim_state
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
FROM fact_sales   AS f
JOIN dim_customer AS cu ON cu.customer_id = f.customer_id
JOIN dim_city     AS ci ON ci.city_id     = cu.city_id
JOIN dim_state    AS st ON st.state_id    = ci.state_id
GROUP BY st.state_name, ci.city_name
ORDER BY revenue DESC
LIMIT 10;


-- =====================================================================
-- 4. BUSINESS-RELEVANT INSIGHTS
--    These answer the key business questions stated in Task 1.1.
-- =====================================================================

-- ---------------------------------------------------------------------
-- Q7. Which sub-categories turned growth into a plateau?
--     Answers business question 2. Compares each sub-category's 2023
--     revenue with its 2024 revenue using conditional aggregation, and
--     ranks by the size of the change.
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
FROM fact_sales       AS f
JOIN dim_date         AS d ON d.order_date      = f.order_date
JOIN dim_sub_category AS s ON s.sub_category_id = f.sub_category_id
JOIN dim_category     AS c ON c.category_id     = s.category_id
WHERE d.year_number IN (2023, 2024)
GROUP BY c.category_name, s.sub_category_name
ORDER BY change_abs ASC;


-- ---------------------------------------------------------------------
-- Q8. Is the Q4 demand peak company-wide or category-specific?
--     Answers business question 3. Quarterly revenue per category across
--     the complete years, with each quarter's share of that category's
--     own annual revenue.
-- ---------------------------------------------------------------------
SELECT
    c.category_name         AS category,
    d.quarter_number        AS quarter,
    COUNT(*)                AS transaction_lines,
    ROUND(SUM(f.amount), 2) AS revenue,
    ROUND(100.0 * SUM(f.amount) / SUM(SUM(f.amount)) OVER (
              PARTITION BY c.category_name), 2)
                            AS pct_of_category_revenue
FROM fact_sales       AS f
JOIN dim_date         AS d ON d.order_date      = f.order_date
JOIN dim_sub_category AS s ON s.sub_category_id = f.sub_category_id
JOIN dim_category     AS c ON c.category_id     = s.category_id
WHERE d.is_complete_year = 1
  AND d.is_complete_month = 1
GROUP BY c.category_name, d.quarter_number
ORDER BY c.category_name, d.quarter_number;
