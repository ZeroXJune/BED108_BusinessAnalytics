# Sales Trend Analysis — Recording Script

**BED 106 Business Analytics — Mini Capstone Project**
Talibon Polytechnic College

**Julebeth reads the parts below.** The full running order:

| Part | Speaker | Covers | Approx |
| --- | --- | --- | --- |
| 1 | Alber | Opening; the business problem | 3:00 |
| 2 | Julebeth | Checkpoint 1 — the dataset, the database, the queries | 8:45 |
| 3 | Alber | The Checkpoint 2 workbook | 1:30 |
| 4 | Mardy | Checkpoint 2 — statistics, correlation, regression, the trend | 8:30 |
| 5 | Alber | The correction, what it means, the questions, the close | 6:00 |

About **28 minutes** at a normal speaking pace — Alber 10:30 across his three
parts, Julebeth 8:45, Mardy 8:30. If you need it shorter, cut the six
limitations down to one line in Part 4 and drop three of the eight questions in
Part 5; that takes off about three minutes without losing a task.

*Lines in italics inside brackets are stage directions — what to have on screen.
Do not read them aloud.*

**One thing before you record.** Section 3.2 of the brief says AI-generated
analysis is not permitted. This script was drafted with AI help, so change the
wording as you go — say it the way you would say it, swap sentences around, cut
what feels stiff. The numbers and the reasoning have to stay; the phrasing
should become yours. Read it through once, then record without staring at the
page.

**Recording notes.** Record your part in one take, screen-recording with audio
rather than filming a monitor. If you stumble, don't stop — pause and repeat the
sentence, and Alber cuts it. Leave two seconds of silence at each end. Agree on
screen resolution and mic distance beforehand so the three parts match. Alber
joins the five files in order, normalises the audio, and puts a two-second title
card at the head of each part.

---

# Part 2 — Julebeth

*[The raw CSV on screen, first 15–20 rows.]*

I'm Julebeth, and I'll take it from the raw file.

This is the export we started with — 1,194 transaction lines, 12 columns,
running from 22 March 2020 to 15 March 2025. The brief asks for at least 200
rows, so we're well past that.

One thing to be clear about first: the grain. Each row here is one product line
on an order, not one order. Three products on an order means three rows.
Everything we do later depends on that.

We ran a quality assessment before touching anything, and we found five
problems.

**First, the Order ID column is not a primary key.** 1,194 rows, but only 547
distinct order IDs — and these aren't duplicate rows. The same ID shows up on
different dates, for different customers. So it identifies neither a row nor an
order.

Why not just repair it? Because repairing it means deciding which of two rows
sharing an ID is the real one, and we have no evidence for that decision. Making
that evidence up is data fabrication, and the brief says that's grounds for a
failing mark. So we kept it as a plain attribute and issued our own key, called
sale_id. It costs us nothing, because no question we ask needs order identity.

**Second, the customer name isn't an identifier either.** 807 customers resolve
from 802 distinct names, because five names appear in more than one city. So our
customer key is the pair — name and city together.

**Third, the Year-Month column is redundant.** You can derive it from the date,
so it doesn't belong in a normalised schema. We rebuilt it in a dates table.

**Fourth, both ends of the file are partial.** It starts on 22 March 2020 and
stops on 15 March 2025. That sounds minor. It isn't — it's where the one real
error in this project came from, and we'll come back to it.

**And fifth, the dataset is synthetic.** It's not real trading data, and we're
saying that up front rather than burying it. We have five pieces of evidence.

There isn't one loss-making line in five years — no real retailer has that. 22
of the 802 names end in credential suffixes like MD or DDS, which is what the
Faker library produces. There are US cities paired with UPI and EMI payment
methods, and those are Indian payment rails. The payment mix is almost perfectly
uniform — 206 to 260 across every single method. And the Amount histogram comes
out flat instead of right-skewed, which is what a random number generator looks
like.

And we didn't fix any of it. Fixing it would mean inventing numbers. So we
stated it, we proved it, and we carried it through as a limitation. The method
isn't affected — every query and every statistic in this project would run
exactly the same way on real data.

*[Switch to the ERD.]*

So we normalised that flat file into a star schema. One fact table, seven
dimension tables around it — eight in total. The fact table is sales, one row per
transaction line, and around it we have customers, cities, states, categories,
sub_categories, payment_modes and dates.

Why a star, instead of the one table we started with? Three reasons.

Consistency — in the flat file a category name is repeated on every row that
uses it, so one typo creates a category that doesn't exist. In the star that
name lives in one place and the fact table just carries an integer key. A typo
goes from unlikely to impossible.

The brief — Task 1.3 wants at least two related tables with proper primary and
foreign keys. What we built has eight tables, eight primary keys, seven foreign
keys, six unique constraints and four check constraints. And we tested that
those constraints actually reject bad rows; we didn't just assume it.

And the queries — the category trend question needs category and date sitting on
the same row as the amount, and a star gives you that in one join.

The dates table looks like overkill until you try to write the queries. It's
there for two reasons. We never call YEAR or strftime anywhere, so the same
query file runs unchanged on MySQL and on SQLite — we verified that. And it
carries two flags the raw dates can't: is_complete_month and is_complete_year.
Those are the fix for problem four, and they're what stops anyone from comparing
a nine-month 2020 against a full 2021.

One thing that cost us real time — year_month is a reserved word in MySQL. Our
CREATE TABLE statement failed outright with a syntax error until we put
backticks around it. And we only found that because we installed an actual MySQL
server and ran the import, instead of assuming the file was fine.

*[Switch to the SHOW TABLES screenshot.]*

The whole thing loads from one file — the database, all eight tables, all the
data. And it ends with a verification block whose last row has to read 1,194
rows, 6,182,639 in revenue, 547 order IDs, 57 complete months, and zero orphaned
rows.

*[Switch to the query screenshots — Q3 first.]*

So with the database built, we could ask the questions. There are eight queries
in four groups: two basic retrievals using WHERE and ORDER BY, two aggregates
using GROUP BY, two multi-table joins — ours each join four tables — and two
business-insight queries. Here's what they found.

**First, growth stopped in 2022, and it stopped in a specific way.** Query 3
aggregates by year, but on a per-month basis, so the partial years can't distort
it. Revenue per month went from 92,934 in 2020, up to 121,648 at the 2022 peak,
then down to 100,207 in 2024. But margin never left that 24-to-27 percent band,
and average order value never left 5,008 to 5,444. Put those together and you
have the diagnosis — fewer orders, not cheaper ones and not less profitable
ones. Which points at demand generation, not at pricing.

*[Switch to Q5.]*

**Second, one sub-category explains most of the gap.** Printers lost 136,865
between 2023 and 2024 — a 71 percent collapse, and on its own that's more than
half the entire gap between the 2022 peak and 2024. Every Electronics
sub-category fell, and the category as a whole is down 40.8 percent. But every
Office Supplies sub-category grew — Paper is up 85,689, which is 149.4 percent.

And that's the point: this is not a general slowdown. Two opposite trends are
running at the same time, and the company-wide figure is just their average,
which describes neither of them. That's the most useful thing Checkpoint 1
produced.

*[Switch to Q8.]*

**Third, seasonality is category-specific.** The blended figure tells you Q4 is
the peak quarter. But split it out, and Electronics actually peaks in Q2, at
30.79 percent of its annual revenue. Furniture peaks in Q4 at 30.84, and Office
Supplies in Q4 at 32.16. So one blended planning curve is wrong for all three —
it over-stocks Electronics in Q4 and under-stocks it in Q2.

**And fourth, geography isn't a factor.** State revenue spans only 28 percent
across five years, and no state trends against the others. Not every finding has
to be a discovery — this one tells the business where not to spend its effort.

So that was Checkpoint 1 — what happened. Checkpoint 2 takes the same data into
Excel and asks how strong the evidence actually is, and what we can predict.

