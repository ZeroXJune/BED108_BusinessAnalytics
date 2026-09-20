# Checkpoint 4, Task 4.2 — Data Ethics, Privacy and Governance

**BED 106 Business Analytics — Mini Capstone Project**

---

## Privacy considerations

The dataset contains what look like personal data: 802 distinct customer
names, each attached to a city, a state, a purchase history and a profit
figure. On the face of it that is exactly the kind of record the Data Privacy
Act is written about.

It is not, and the reason matters more than the conclusion. During Checkpoint 1
we established with five independent machine-checked signals that **the dataset
is synthetic** — generated, not collected. Twenty-two of the 802 names end in
credential suffixes such as "MD" or "DDS", which is a known artefact of the
Faker library. US cities are paired with UPI and EMI payment methods, which are
Indian payment rails. There is not one loss-making line across five years, the
payment mix is near-uniform at 206 to 260 across every method, and the
transaction-amount histogram is flat rather than right-skewed. Our own
Checkpoint 2 descriptive statistics confirmed that flatness independently.

Because the names are generated, **there is no data subject**. No living person
is identified or identifiable in this file, so the Data Privacy Act is not
engaged and there was nothing to anonymise. We therefore did not anonymise the
names, and we want to be precise about why: not because the dataset is
published on a public platform, but because the individuals in it do not exist.

That distinction is the single most important point in this reflection.
**Public availability is not consent.** A dataset being downloadable does not
make the people inside it willing participants in our analysis. Had these
names been real, the fact that someone uploaded them to a public repository
would not have given us a lawful basis to process them, and the correct
response would have been to pseudonymise the customer dimension — replacing
names with surrogate keys, which our schema already uses — before any analysis
began. Our star schema is structured so that this would have been a one-table
change: `customers` holds the only identifying attribute, and every other table
references it by integer key.

## Ethical issues

Two concerns arise from our own work rather than from the data.

The first is **the segmentation we built in Checkpoint 3**. We clustered 807
customers and labelled one group of 350 "Thin-Margin Buyers" — 43% of
customers, a third of revenue, and under a fifth of the profit. That label is
analytically accurate and commercially useful, and it is also the most
ethically loaded object in this project. A business acting on it could
rationally decide to deprioritise service, withdraw discounts, or stop
marketing to those accounts. If the segmentation correlates with something it
should not — income, location, or the kind of product a household needs — then
an apparently neutral margin calculation becomes a mechanism for treating
poorer customers worse. We checked whether geography drives the segments and it
does not, but on real data that check would need to be repeated for every
protected characteristic available, and the segment definitions published to
the people they affect rather than kept internal.

The second is **survivorship and coverage bias**. The dataset records
transactions that happened. It contains no record of customers who considered a
purchase and did not make one, no competitor pricing, and no stockouts. Our
central finding — that the company writes fewer orders rather than worse ones —
is therefore a statement about what was sold, not about demand. A model built
only on completed transactions will always attribute a decline to the
customers who remain rather than to the ones who left, and it cannot see the
latter at all.

We also carried a deliberate constraint throughout: **we did not fabricate
corrections**. When we found that `Order ID` did not identify an order, the
repair would have required deciding which of two conflicting rows was real, and
we had no evidence for that decision. Inventing it would have been data
fabrication. We documented the defect instead and worked around it.

## Data governance

The dataset is a third-party publication. We do not own it; we hold it under
whatever licence the publisher attached, and the group's Checkpoint 1
documentation records the source, the access date and the licence terms. We
have no right to re-licence it or to represent its contents as describing a
real company, which is why every report in this project states the synthetic
limitation rather than burying it.

A responsible governance framework for a dataset like this, were it real, would
need four things. **Ownership**: a named data owner accountable for the
customer dimension, distinct from the analysts using it. **Access control**:
analysts working against the pseudonymised views rather than the base tables,
with the name-to-key mapping held separately and access logged. **Retention**:
a defined period after which transaction-level personal data is aggregated away,
since our monthly and category analyses need none of it — every finding in
Checkpoints 2 and 3 except the customer segmentation would survive the deletion
of every name in the file. **Lineage**: the reproducible pipeline this project
already has, where `clean_and_load.py` regenerates the database from the
untouched raw file, so any figure can be traced back to a source row.

## Regulatory awareness

**Republic Act No. 10173, the Data Privacy Act of 2012**, governs the
processing of personal information in the Philippines. It defines personal
information as any data from which an individual's identity is apparent or can
reasonably be ascertained, and requires a lawful basis for processing, a
declared and legitimate purpose, and proportionality — only as much data as the
purpose needs. It establishes the rights of data subjects to be informed, to
access, to object, and to rectification, and it obliges personal information
controllers to implement organisational and technical security measures. The
National Privacy Commission enforces it.

Applied to this project: the synthetic nature of the file means no processing
of personal information occurred. Applied to the same analysis on real customer
data, three of the Act's principles would bite immediately. **Proportionality**
would question why analysts need customer names at all when surrogate keys
serve every purpose. **Purpose specification** would require that "sales trend
analysis" be declared to the data subjects, and would not cover reusing the
segmentation for pricing decisions later. And the **right to object** would
give a customer grounds to challenge being placed in a margin-based segment
that affects the service they receive.

The EU's **General Data Protection Regulation** reaches the same conclusions
through stricter machinery — an explicit lawful basis, data protection by design
and by default, and in Article 22 a right not to be subject to solely automated
decisions with legal or similarly significant effects. Our clustering is not
automated decision-making today, because a person would decide what to do with
the segments. It would become so the moment a system withheld a discount on the
strength of a cluster label, and that line is much closer than it looks.
