# Checkpoint 1 — Rubric Compliance Map

Every requirement in the BED 106 project brief for Checkpoint 1, mapped to
where it is satisfied. Items marked **ACTION** need something only the group
can supply.

## Tasks & Deliverables

| Brief requirement | Status | Where |
| --- | --- | --- |
| **1.1** Business domain and specific problem | Done | Report, Task 1.1 — Retail & Sales Analytics |
| **1.1** Why the problem matters (impact) | Done | Report, "Business Impact & Significance" |
| **1.1** Key business questions | Done | Three questions, each mapped to the queries that answer it |
| **1.1** Data type planned and source | Done | Report, "Data Source Overview" |
| **1.2** Dataset name, source URL/file, date accessed, licence | Partial | Table 2 — **ACTION: confirm the exact licence** |
| **1.2** Data dictionary (name, type, description) | Done | Table 3, all 12 columns |
| **1.2** Quality assessment: missing, duplicates, inconsistencies, cleaning | Done | Report §"Preliminary Data Quality Assessment"; evidence in `reports/data_quality_report.md` |
| **1.2** Raw dataset preview, first 10–20 rows | Partial | Table 4 — **ACTION: paste your own screenshot** |
| **1.3** ERD with at least 2 related tables | Exceeded | 7 tables, `docs/erd.md` |
| **1.3** Tables with appropriate types and PK/FK | Done | `sql/01_schema_mysql.sql` |
| **1.3** Import and load cleaned data | Done | `sql/03_insert_data.sql`, 1,194 fact rows |
| **1.3** Screenshots of schema and populated tables | Not done | **ACTION: screenshot your own RDBMS run** |
| **1.4** ≥2 SELECT with WHERE and ORDER BY | Done | Q1, Q2 |
| **1.4** ≥2 GROUP BY with aggregates | Done | Q3, Q4 (COUNT, SUM, AVG) |
| **1.4** ≥2 JOIN queries, 2+ tables | Exceeded | Q5, Q6 — four tables each |
| **1.4** ≥2 business-relevant queries answering the key questions | Done | Q7, Q8 |
| **1.4** For each query: SQL code | Done | `sql/04_queries.sql`, commented |
| **1.4** For each query: output/result screenshot | Partial | Full result sets in `reports/query_results.md` — **ACTION: screenshot your own run** |
| **1.4** For each query: 2–3 sentence business interpretation | See note | Present, but longer than 2–3 sentences — **see the note below** |

## General guidelines (Section 3.1)

| Requirement | Status |
| --- | --- |
| Arial 12pt | Done |
| 1-inch margins | Done |
| 1.5 line spacing | Done |
| Section headings clearly and consistently labelled | Done |
| Figures, tables and charts numbered and captioned | Done — 12 tables, 3 figures |
| Cover page: course code and title, project title, members and roles, submission date, academic year | Done — **ACTION: fill the blanks** |
| Dataset minimum 200 rows | Done — 1,194 rows |

## Submission requirements

| Requirement | Status |
| --- | --- |
| Printed and bound report (Tasks 1.1–1.4) | Ready to print — `reports/Checkpoint_1_Report.docx` |
| SQL script file (.sql) via class portal | Ready — `sql/01_schema_mysql.sql`, `sql/03_insert_data.sql`, `sql/04_queries.sql` |
| Signed Individual Contribution Form | Template at `reports/Form_A_Individual_Contribution.md` — **ACTION: complete and sign, one per member** |
| Deadline: end of Week 4 laboratory session | — |

## Note on the written interpretations

Section 3.2 of the brief states that **AI-generated analysis is not permitted**
and that insights must be derived by the students themselves. The business
interpretations currently in the report were drafted with AI assistance and
**must be rewritten by the group in their own words** before submission.

The underlying material is not affected by this: the query results in
`reports/query_results.md` are computed output, and the schema and SQL are
tooling. What must be your own is the *reading* of those numbers — the
"what this means for the business" prose under each query.

The rubric also asks for 2–3 sentences per query; the current drafts are
longer. Rewriting them shorter and in your own voice satisfies both points at
once. The instructor may ask any member to explain any part of the project, so
the group needs to be able to defend every claim regardless.
