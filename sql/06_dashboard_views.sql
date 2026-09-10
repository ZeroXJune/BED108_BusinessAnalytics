-- =====================================================================
-- BED 106 Business Analytics — Mini Capstone, Checkpoint 3
-- Dashboard views
--
-- Five views that a BI tool connects to instead of querying the star
-- schema directly. Each one is a single grain, already joined and
-- labelled, so the dashboard does no arithmetic that this file cannot
-- be held to.
--
-- Runs unchanged on MySQL 8 and SQLite 3: no YEAR(), no strftime(), no
-- window functions. Calendar parts come from `dates`, as everywhere
-- else in this project.
--
--   mysql -u root -p sales_trend < sql/06_dashboard_views.sql
-- =====================================================================


-- ---------------------------------------------------------------------
-- v_sales_detail — one row per transaction line, fully labelled.
-- The base for anything the aggregate views do not cover. Carries the
-- completeness flags so a dashboard filter can exclude partial periods
-- rather than silently comparing a nine-month year against a full one.
-- ---------------------------------------------------------------------
DROP VIEW IF EXISTS v_sales_detail;
CREATE VIEW v_sales_detail AS
SELECT
    s.sale_id,
    s.order_ref,
    s.order_date,
    d.year_number,
    d.quarter_number,
    d.month_number,
    d.month_name,
    d.year_month,
    d.is_complete_month,
    d.is_complete_year,
    c.customer_name,
    ci.city_name,
    st.state_name,
    cat.category_name,
    sc.sub_category_name,
    pm.payment_mode_name,
    s.quantity,
    s.amount,
    s.profit
FROM sales s
JOIN dates          d   ON d.order_date       = s.order_date
JOIN customers      c   ON c.customer_id      = s.customer_id
JOIN cities         ci  ON ci.city_id         = c.city_id
JOIN states         st  ON st.state_id        = ci.state_id
JOIN sub_categories sc  ON sc.sub_category_id = s.sub_category_id
JOIN categories     cat ON cat.category_id    = sc.category_id
JOIN payment_modes  pm  ON pm.payment_mode_id = s.payment_mode_id;


-- ---------------------------------------------------------------------
-- v_monthly — one row per complete calendar month.
--
-- 59 rows, not 57. `is_complete_month` admits January and February 2025,
-- which are whole months but sit outside the Checkpoint 2 analysis
-- window — they are the two holdout months the forecast was tested
-- against. `in_analysis_window` marks the 57 months the regression was
-- fitted on (April 2020 to December 2024), so a dashboard filtered on
-- that column agrees with the Checkpoint 2 report exactly, and one that
-- is not can still show the holdout.
--
-- Note that `is_complete_year` means "inside the analysis window", not
-- "twelve months": 2020 carries it while holding nine months, because
-- its partial start is handled by `is_complete_month` and by measuring
-- per month rather than per year.
-- ---------------------------------------------------------------------
DROP VIEW IF EXISTS v_monthly;
CREATE VIEW v_monthly AS
SELECT
    d.year_month,
    d.year_number,
    d.quarter_number,
    d.month_number,
    d.month_name,
    COUNT(*)                                    AS transaction_lines,
    SUM(s.quantity)                             AS units_sold,
    SUM(s.amount)                               AS revenue,
    SUM(s.profit)                               AS profit,
    ROUND(SUM(s.amount) * 1.0 / COUNT(*), 2)    AS avg_line_value,
    ROUND(100.0 * SUM(s.profit)
          / NULLIF(SUM(s.amount), 0), 2)        AS margin_pct,
    MAX(d.is_complete_year)                     AS in_analysis_window
FROM sales s
JOIN dates d ON d.order_date = s.order_date
WHERE d.is_complete_month = 1
GROUP BY d.year_month, d.year_number, d.quarter_number,
         d.month_number, d.month_name;


-- ---------------------------------------------------------------------
-- v_category_month — category and sub-category by month.
-- Feeds the mix visuals: the Printer collapse and the Office Supplies
-- growth are both only visible at this grain.
-- ---------------------------------------------------------------------
DROP VIEW IF EXISTS v_category_month;
CREATE VIEW v_category_month AS
SELECT
    d.year_month,
    d.year_number,
    d.quarter_number,
    cat.category_name,
    sc.sub_category_name,
    COUNT(*)                                    AS transaction_lines,
    SUM(s.quantity)                             AS units_sold,
    SUM(s.amount)                               AS revenue,
    SUM(s.profit)                               AS profit,
    ROUND(100.0 * SUM(s.profit)
          / NULLIF(SUM(s.amount), 0), 2)        AS margin_pct
FROM sales s
JOIN dates          d   ON d.order_date       = s.order_date
JOIN sub_categories sc  ON sc.sub_category_id = s.sub_category_id
JOIN categories     cat ON cat.category_id    = sc.category_id
WHERE d.is_complete_month = 1
GROUP BY d.year_month, d.year_number, d.quarter_number,
         cat.category_name, sc.sub_category_name;


-- ---------------------------------------------------------------------
-- v_geography — state and city totals.
-- Checkpoint 1 found geography is not a driver, so this exists to let a
-- viewer confirm that for themselves rather than take it on trust.
-- ---------------------------------------------------------------------
DROP VIEW IF EXISTS v_geography;
CREATE VIEW v_geography AS
SELECT
    st.state_name,
    ci.city_name,
    COUNT(*)                                    AS transaction_lines,
    COUNT(DISTINCT s.customer_id)               AS customers,
    SUM(s.amount)                               AS revenue,
    SUM(s.profit)                               AS profit,
    ROUND(SUM(s.amount) * 1.0
          / NULLIF(COUNT(DISTINCT s.customer_id), 0), 2)
                                                AS revenue_per_customer,
    ROUND(100.0 * SUM(s.profit)
          / NULLIF(SUM(s.amount), 0), 2)        AS margin_pct
FROM sales s
JOIN customers c  ON c.customer_id = s.customer_id
JOIN cities    ci ON ci.city_id    = c.city_id
JOIN states    st ON st.state_id   = ci.state_id
GROUP BY st.state_name, ci.city_name;


-- ---------------------------------------------------------------------
-- v_annual — one row per year in the analysis window, measured per month.
--
-- Per month, not per year: 2020 holds nine months, and comparing its
-- part-year total against a full 2021 is the error Checkpoint 2 caught.
-- 2025 is excluded outright — two months of it would produce a
-- revenue-per-month figure that looks comparable and is not.
-- ---------------------------------------------------------------------
DROP VIEW IF EXISTS v_annual;
CREATE VIEW v_annual AS
SELECT
    d.year_number,
    COUNT(DISTINCT d.year_month)                AS months_covered,
    COUNT(*)                                    AS transaction_lines,
    SUM(s.quantity)                             AS units_sold,
    SUM(s.amount)                               AS revenue,
    SUM(s.profit)                               AS profit,
    ROUND(SUM(s.amount) * 1.0
          / NULLIF(COUNT(DISTINCT d.year_month), 0), 2)
                                                AS revenue_per_month,
    ROUND(SUM(s.amount) * 1.0 / COUNT(*), 2)    AS avg_line_value,
    ROUND(100.0 * SUM(s.profit)
          / NULLIF(SUM(s.amount), 0), 2)        AS margin_pct
FROM sales s
JOIN dates d ON d.order_date = s.order_date
WHERE d.is_complete_month = 1
  AND d.is_complete_year  = 1
GROUP BY d.year_number;
