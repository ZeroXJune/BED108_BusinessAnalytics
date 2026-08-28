# Screenshot Guide — Checkpoint 1

Which query fills which slot in the report, what to capture, and what the
result should say. The script is **`sql/05_screenshot_queries.sql`**.

## Before you start

Load the database. **One file does everything** — creates the database, all 8
tables with their keys and constraints, and all the data:

**phpMyAdmin:** *Import* tab → *Choose File* → `sql/02_mysql_full_import.sql`
→ *Go*. No database needs to exist first; the file creates it.

**Workbench:** *File → Open SQL Script* → `sql/02_mysql_full_import.sql` →
click the lightning bolt.

**Terminal:** `mysql -u root -p < sql/02_mysql_full_import.sql`

It ends with its own verification. The final result must read exactly:

```
1194 | 6182639.00 | 547 | 57 | 0 | 0
```

If it does, the load is correct and you can start capturing.

> The two-file route still works if you prefer it —
> `01_schema_mysql.sql` then `03_insert_data.sql` — but note the second file
> has no `USE` statement (so that it also runs on SQLite), so you must select
> the database yourself:
> `mysql -u root -p sales_trend < sql/03_insert_data.sql`.

> **All of this was tested.** The import and all sixteen blocks below were run
> against a real MariaDB 10.11 server, not just checked by eye. The row counts
> and every figure in the "Expected result" columns are what the server
> actually returned.

In **phpMyAdmin**: select the `sales_trend` database → **SQL** tab → paste one
block → **Go**. In **MySQL Workbench**: open the script, put the cursor in a
block, press **Ctrl+Enter** to run just that statement.

## Capture rule

Every screenshot must show **the SQL and its result in the same image**. A
result grid with no visible query proves nothing, and the Documentation
criterion (20 pts) explicitly asks for labelled screenshots.

In phpMyAdmin the SQL box stays above the results — capture both. In Workbench,
drag the results pane up so the query and the first rows fit together.

---

## Part A — Task 1.3 slots (schema and populated tables)

| Block | Report slot | Capture | Expected result |
| --- | --- | --- | --- |
| **S1** | Schema | `SHOW TABLES;` | Exactly **8** tables |
| **S2** | Schema | `DESCRIBE sales;` | 9 columns, `sale_id` marked **PRI** |
| **S3** | Schema — *the key one* | `SHOW CREATE TABLE sales;` | 4 FOREIGN KEYs, 2 CHECKs, 4 indexes, all in one image |
| **S4** | Schema | Foreign-key listing | **7** rows, parent → child |
| **S5** | Populated tables | Row counts | 3, 18, 807, 648, 5, 6, 12, **1194** |
| **S6** | Populated tables | Integrity proof | `1194 | 6182639 | 547 | 57 | 0 | 0` |
| **S7** | Task 1.2 duplicates | The reused Order ID | 3 rows, same `order_ref`, 3 different customers |

**S3 is the one to lead with.** It shows data types, the primary key, all four
foreign keys, both CHECK constraints and the indexes in a single image — it
covers most of the Data Preparation criterion (25 pts) by itself.

**S6 is worth more than it looks.** The last two columns are orphan-row counts
and both must be **0**. That is direct evidence of referential integrity, not
just that rows loaded. Say so in the caption.

**S7 is your evidence for the Task 1.2 duplicate discussion** — one `order_ref`
appearing against three dates and three different customers in three states.
It is the reason the fact table uses a surrogate `sale_id`.

---

## Part B — Task 1.4 slots (the eight queries)

Each needs three things per the brief: **(a)** the SQL, **(b)** the result,
**(c)** a 2–3 sentence business interpretation in your own words.

| Block | Group | Requirement met | Expected result |
| --- | --- | --- | --- |
| **Q1** | Basic retrieval | SELECT, WHERE, ORDER BY | 15 rows, amount 9,914 → 9,380 |
| **Q2** | Basic retrieval | SELECT, WHERE, ORDER BY | 15 rows; worst is `sale_id` 8 at **0.78%** margin |
| **Q3** | Aggregate | GROUP BY, COUNT, SUM, AVG | 5 rows; 2020 shows **9** months; 2022 peaks at 121,647.92/month |
| **Q4** | Aggregate | GROUP BY, COUNT, SUM, AVG | 12 rows; December **11.09%**, January **4.73%** |
| **Q5** | Join (4 tables) | 2+ tables joined | 15 rows; Electronics 538,319 → **318,630** |
| **Q6** | Join (4 tables) | 2+ tables joined | 10 rows; Orlando first, 452,158 and 9,829.52/customer |
| **Q7** | Business insight | Answers question 2 | 12 rows; Printers **−136,865 (−71.0%)**, Paper **+85,689 (+149.4%)** |
| **Q8** | Business insight | Answers question 3 | 12 rows; Electronics peaks **Q2 (30.79%)**, others Q4 |

> **One cell differs between engines, by design of their rounding.** In Q3 the
> 2024 `avg_line_value` is exactly 5010.325. MySQL's `ROUND` rounds half away
> from zero and shows **5010.33**; SQLite and Python round half to even and show
> **5010.32**. Your MySQL screenshot showing 5010.33 is correct. Every other
> value across all eight queries is identical on both engines.

### A trap worth knowing: `year_month` is a reserved word

`YEAR_MONTH` is a reserved word in MySQL and MariaDB — it is the unit in
`INTERVAL 1 YEAR_MONTH`. So this **fails**:

```sql
SELECT year_month FROM dates;          -- syntax error
```

and these both **work**:

```sql
SELECT dates.year_month FROM dates; -- qualified with the table name
SELECT `year_month` FROM dates;        -- wrapped in backticks
```

Every query in this project qualifies or backticks it, so the supplied scripts
run fine. It only bites if you type a quick query of your own. It is also a
good thing to be able to explain if you are asked why the schema has backticks
in it.

### If Q8 fails

Q8 uses a window function (`OVER (PARTITION BY ...)`), which needs **MySQL 8.0
or later**. On MySQL 5.7 you get a syntax error near `OVER`.

Use **Q8-ALT** instead — it is at the end of the script and produces
**identical numbers** using a correlated subquery. Verified: both return the
same 12 rows. Check your version first with `SELECT VERSION();`.

---

## What examiners look for

- **The `months_covered` column in Q3** is deliberate. 2020 shows 9 because the
  file starts on 22 March 2020, so years must be compared on
  `revenue_per_month`, not `revenue`. If asked why, that is the answer — and it
  is the kind of thing that earns marks rather than losing them.
- **Q7 is your headline.** Printers alone lost more than half the entire
  peak-to-2024 revenue gap. Give it the largest, clearest screenshot.
- **Label every image** in the report: "Figure 5 — Q3 annual sales trend" and
  so on. Unlabelled screenshots cost Documentation marks.

## Checklist before you print

- [ ] 7 Part A screenshots captured (S1–S7)
- [ ] 8 Part B screenshots captured (Q1–Q8)
- [ ] Every image shows the SQL *and* the result
- [ ] Every image is numbered and captioned
- [ ] Each of Q1–Q8 has a 2–3 sentence interpretation **in your own words**
- [ ] Numbers on screen match the "Expected result" column above
