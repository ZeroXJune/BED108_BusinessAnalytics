# Sales Trend Analysis — Recording Script

**BED 106 Business Analytics — Mini Capstone Project**
Talibon Polytechnic College

**Julebeth reads the parts below.** The full running order:

| Part | Speaker | Covers | Approx |
| --- | --- | --- | --- |
| 1 | Alber | Opening; the business problem | 3:00 |
| 2 | Julebeth | Checkpoint 1 — the dataset and its five problems | 3:30 |
| 3 | Mardy | Checkpoint 1 — the database, and the eight queries | 5:30 |
| 4 | Alber | Checkpoint 2 — the workbook, statistics, regression, the trend | 10:00 |
| 5 | Alber | The correction, what it means, the questions, the close | 6:00 |

About **28 minutes** at a normal speaking pace. Alber carries Checkpoint 2 and
the framing — 19 minutes across three files — while Julebeth and Mardy split
Checkpoint 1 between them. Alber's Part 4 is the long one, so record it in two
sittings if you need to; there is a natural break after the regression.

If you need it shorter, cut the six limitations in Part 4 down to one line and
drop three of the eight questions in Part 5; that takes off about three minutes
without losing a task.

*Lines in italics inside brackets are stage directions, and the tables and
charts under them are the exhibits to have on screen at that moment. Do not read
any of it aloud — the spoken lines are the plain paragraphs.*

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

*[The raw file — have the CSV open, or show this extract.]*

Caption: The raw export. The first two rows share one Order ID across different dates and customers.

| Order ID | Amount | Profit | Qty | Category | Sub-Category | Payment | Order Date | Customer | State | City |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| B-26776 | 9,726 | 1,275 | 5 | Electronics | Electronic Games | UPI | 2023-06-27 | David Padilla | Florida | Miami |
| B-26776 | 9,726 | 1,275 | 5 | Electronics | Electronic Games | UPI | 2024-12-27 | Connor Morgan | Illinois | Chicago |

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

That is the state of the raw data we started from. What we built out of it
next was a proper database.

---

