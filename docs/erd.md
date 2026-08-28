# Entity-Relationship Diagram — `sales_trend`

Checkpoint 1, Task 1.3. Star schema: one fact table (`sales`) at the grain of a
single transaction line, surrounded by seven dimensions. `PK` marks a
primary key, `FK` a foreign key.

```mermaid
erDiagram
    states ||--o{ cities : "is located in"
    cities ||--o{ customers : "is home to"
    categories ||--o{ sub_categories : "contains"
    customers ||--o{ sales : "places"
    sub_categories ||--o{ sales : "is sold as"
    payment_modes ||--o{ sales : "pays for"
    dates ||--o{ sales : "occurs on"

    states {
        INT state_id PK
        VARCHAR state_name
    }
    cities {
        INT city_id PK
        VARCHAR city_name
        INT state_id FK
    }
    customers {
        INT customer_id PK
        VARCHAR customer_name
        INT city_id FK
    }
    categories {
        INT category_id PK
        VARCHAR category_name
    }
    sub_categories {
        INT sub_category_id PK
        VARCHAR sub_category_name
        INT category_id FK
    }
    payment_modes {
        INT payment_mode_id PK
        VARCHAR payment_mode_name
    }
    dates {
        DATE order_date PK
        SMALLINT year_number
        TINYINT quarter_number
        TINYINT month_number
        VARCHAR month_name
        CHAR year_month
        TINYINT is_complete_year
    }
    sales {
        INT sale_id PK
        VARCHAR order_ref
        DATE order_date FK
        INT customer_id FK
        INT sub_category_id FK
        INT payment_mode_id FK
        INT quantity
        DECIMAL amount
        DECIMAL profit
    }
```

## Relationships in words

| Parent | Child | Cardinality | Meaning |
| --- | --- | --- | --- |
| `states` | `cities` | 1 : many | Each of the 6 states holds 3 cities. |
| `cities` | `customers` | 1 : many | Each customer belongs to exactly one city. |
| `categories` | `sub_categories` | 1 : many | Each of the 3 categories holds 4 sub-categories. |
| `customers` | `sales` | 1 : many | A customer can appear on many transaction lines. |
| `sub_categories` | `sales` | 1 : many | A sub-category is sold on many lines. |
| `payment_modes` | `sales` | 1 : many | A payment method is used on many lines. |
| `dates` | `sales` | 1 : many | A calendar date carries many lines. |

## Fact and dimension roles

The tables are named plainly, without `fact_`/`dim_` prefixes, but they play the
two standard roles of a star schema:

| Role | Tables | Why |
| --- | --- | --- |
| Fact | `sales` | Holds the additive measures (`quantity`, `amount`, `profit`) at a grain of one transaction line. |
| Dimension | `states`, `cities`, `customers`, `categories`, `sub_categories`, `payment_modes`, `dates` | Hold the descriptive attributes the measures are sliced by. |

## Design notes

- **Grain.** One row of `sales` is one product line on one order. All
  measures (`quantity`, `amount`, `profit`) are additive at this grain.
- **Surrogate key.** The raw `Order ID` is reused across different dates
  and customers, so it cannot be a primary key. It is retained as the
  descriptive column `order_ref` and the table is keyed on `sale_id`.
- **Why a date dimension.** Pre-computing year, quarter, month and the
  `is_complete_year` flag keeps the trend queries free of dialect-specific
  date functions and makes the partial-2025 exclusion explicit rather than
  buried in a `WHERE` clause on raw dates.
- **Snowflaked dimensions.** Geography (`state → city → customer`) and
  product (`category → sub_category`) are kept as separate tables rather
  than flattened, so that Task 1.4 has genuine multi-table joins to
  demonstrate and so a city can be renamed in one place.
