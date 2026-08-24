# Entity-Relationship Diagram — `sales_trend`

Checkpoint 1, Task 1.3. Star schema: one fact table at the grain of a
single transaction line, surrounded by six dimensions. `PK` marks a
primary key, `FK` a foreign key.

```mermaid
erDiagram
    dim_state ||--o{ dim_city : "is located in"
    dim_city ||--o{ dim_customer : "is home to"
    dim_category ||--o{ dim_sub_category : "contains"
    dim_customer ||--o{ fact_sales : "places"
    dim_sub_category ||--o{ fact_sales : "is sold as"
    dim_payment_mode ||--o{ fact_sales : "pays for"
    dim_date ||--o{ fact_sales : "dates"

    dim_state {
        INT state_id PK
        VARCHAR state_name
    }
    dim_city {
        INT city_id PK
        VARCHAR city_name
        INT state_id FK
    }
    dim_customer {
        INT customer_id PK
        VARCHAR customer_name
        INT city_id FK
    }
    dim_category {
        INT category_id PK
        VARCHAR category_name
    }
    dim_sub_category {
        INT sub_category_id PK
        VARCHAR sub_category_name
        INT category_id FK
    }
    dim_payment_mode {
        INT payment_mode_id PK
        VARCHAR payment_mode_name
    }
    dim_date {
        DATE order_date PK
        SMALLINT year_number
        TINYINT quarter_number
        TINYINT month_number
        VARCHAR month_name
        CHAR year_month
        TINYINT is_complete_year
    }
    fact_sales {
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
| `dim_state` | `dim_city` | 1 : many | Each of the 6 states holds 3 cities. |
| `dim_city` | `dim_customer` | 1 : many | Each customer belongs to exactly one city. |
| `dim_category` | `dim_sub_category` | 1 : many | Each of the 3 categories holds 4 sub-categories. |
| `dim_customer` | `fact_sales` | 1 : many | A customer can appear on many transaction lines. |
| `dim_sub_category` | `fact_sales` | 1 : many | A sub-category is sold on many lines. |
| `dim_payment_mode` | `fact_sales` | 1 : many | A payment method is used on many lines. |
| `dim_date` | `fact_sales` | 1 : many | A calendar date carries many lines. |

## Design notes

- **Grain.** One row of `fact_sales` is one product line on one order. All
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
