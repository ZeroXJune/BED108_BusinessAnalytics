// =====================================================================
// BED 106 — Checkpoint 3 dashboard
// Power Query: loads every table for the dashboard in one step.
//
// HOW TO USE
//   1. Power BI Desktop → Home → Transform data → New Source → Blank query
//   2. Home → Advanced Editor → replace everything with this file
//   3. Change FolderPath below to where data\dashboard lives on your machine
//   4. Done → then right-click the query → Reference, once per table,
//      and pick the matching field (Monthly, CategoryMonth, ...)
//
// Or, far simpler: Get data → Text/CSV, once per file, and let Power BI
// detect the types. This script exists so the types are right the first
// time rather than after the first wrong chart.
// =====================================================================
let
    // ---- CHANGE THIS to your own path -----------------------------------
    FolderPath = "C:\Users\YourName\Documents\BED106\data\dashboard\",

    Read = (name as text) as table =>
        Csv.Document(
            File.Contents(FolderPath & name),
            [Delimiter = ",", Encoding = 65001, QuoteStyle = QuoteStyle.Csv]
        ),
    Promote = (t as table) as table => Table.PromoteHeaders(t, [PromoteAllScalars = true]),

    // ---- Monthly: the series every trend visual is built on -------------
    // 59 rows. in_analysis_window marks the 57 the Checkpoint 2 regression
    // was fitted on — filter visuals to 1 or the dashboard will disagree
    // with the report.
    Monthly = Table.TransformColumnTypes(Promote(Read("monthly.csv")), {
        {"year_month", type text}, {"month_start", type date},
        {"year_number", Int64.Type}, {"quarter_number", Int64.Type},
        {"month_number", Int64.Type}, {"month_name", type text},
        {"transaction_lines", Int64.Type}, {"units_sold", Int64.Type},
        {"revenue", type number}, {"profit", type number},
        {"avg_line_value", type number}, {"margin_pct", type number},
        {"in_analysis_window", Int64.Type}}),

    // ---- Category by month: everything on page 2 ------------------------
    CategoryMonth = Table.TransformColumnTypes(Promote(Read("category_month.csv")), {
        {"year_month", type text}, {"month_start", type date},
        {"year_number", Int64.Type}, {"quarter_number", Int64.Type},
        {"category_name", type text}, {"sub_category_name", type text},
        {"transaction_lines", Int64.Type}, {"units_sold", Int64.Type},
        {"revenue", type number}, {"profit", type number},
        {"margin_pct", type number}}),

    // ---- Line detail: the page 3 scatter, and anything ad hoc -----------
    Sales = Table.TransformColumnTypes(Promote(Read("sales_detail.csv")), {
        {"sale_id", Int64.Type}, {"order_ref", type text},
        {"order_date", type date}, {"customer_id", Int64.Type},
        {"year_number", Int64.Type},
        {"quarter_number", Int64.Type}, {"month_number", Int64.Type},
        {"month_name", type text}, {"year_month", type text},
        {"month_start", type date},
        {"is_complete_month", Int64.Type}, {"is_complete_year", Int64.Type},
        {"customer_name", type text}, {"city_name", type text},
        {"state_name", type text}, {"category_name", type text},
        {"sub_category_name", type text}, {"payment_mode_name", type text},
        {"quantity", Int64.Type}, {"amount", type number},
        {"profit", type number}}),

    Geography = Table.TransformColumnTypes(Promote(Read("geography.csv")), {
        {"state_name", type text}, {"city_name", type text},
        {"transaction_lines", Int64.Type}, {"customers", Int64.Type},
        {"revenue", type number}, {"profit", type number},
        {"revenue_per_customer", type number}, {"margin_pct", type number}}),

    Annual = Table.TransformColumnTypes(Promote(Read("annual.csv")), {
        {"year_number", Int64.Type}, {"months_covered", Int64.Type},
        {"transaction_lines", Int64.Type}, {"units_sold", Int64.Type},
        {"revenue", type number}, {"profit", type number},
        {"revenue_per_month", type number}, {"avg_line_value", type number},
        {"margin_pct", type number}}),

    CustomerSegments = Table.TransformColumnTypes(
        Promote(Read("customer_segments.csv")), {
        {"customer_id", Int64.Type}, {"customer_name", type text},
        {"city_name", type text}, {"state_name", type text},
        {"transaction_lines", Int64.Type}, {"revenue", type number},
        {"profit", type number}, {"margin_pct", type number},
        {"recency_days", Int64.Type}, {"cluster", Int64.Type},
        {"segment", type text}}),

    SubcategorySegments = Table.TransformColumnTypes(
        Promote(Read("subcategory_segments.csv")), {
        {"sub_category_name", type text}, {"category_name", type text},
        {"revenue_total", type number}, {"revenue_2023", type number},
        {"revenue_2024", type number}, {"growth_pct", type number},
        {"margin_pct", type number}, {"cluster", Int64.Type},
        {"segment", type text}}),

    // ---- Date table: needed for a continuous axis and any time logic ----
    // Built from the data's own range so it can never drift from it.
    FirstDate = List.Min(Sales[order_date]),
    LastDate  = List.Max(Sales[order_date]),
    DayCount  = Duration.Days(LastDate - FirstDate) + 1,
    DateTable = Table.TransformColumnTypes(
        Table.FromRecords(
            List.Transform(List.Dates(FirstDate, DayCount, #duration(1,0,0,0)),
                each [
                    Date         = _,
                    Year         = Date.Year(_),
                    Quarter      = "Q" & Text.From(Date.QuarterOfYear(_)),
                    MonthNumber  = Date.Month(_),
                    MonthName    = Date.MonthName(_),
                    MonthStart   = Date.StartOfMonth(_),
                    YearMonth    = Date.ToText(_, "yyyy-MM")
                ])),
        {{"Date", type date}, {"Year", Int64.Type}, {"Quarter", type text},
         {"MonthNumber", Int64.Type}, {"MonthName", type text},
         {"MonthStart", type date}, {"YearMonth", type text}}),

    Output = [
        Monthly = Monthly, CategoryMonth = CategoryMonth, Sales = Sales,
        Geography = Geography, Annual = Annual,
        CustomerSegments = CustomerSegments,
        SubcategorySegments = SubcategorySegments, DateTable = DateTable
    ]
in
    Output
