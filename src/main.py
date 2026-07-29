from data_loader import DataLoader
from database import Database
from cleaner import Cleaner
from analyzer import Analyzer

# Load data
loader = DataLoader("data/raw/sales.csv")
db = Database("data/analytics.db")

df = loader.load_data()

# # Show original dataset
# loader.show_summary(df)
# loader.preview_data(df)

# Database
db.connect()

table_name = "sales"

# Save raw data
db.save_dataframe(df, table_name)
# db.verify_row_count(table_name)

# Clean data
cleaner = Cleaner()
cleaned_df = cleaner.clean_data(df)

# Validate cleaned data
cleaner.validate_data(cleaned_df)

loader.show_summary(cleaned_df)
loader.preview_data(cleaned_df)

# Save cleaned CSV
cleaner.save_cleaned_data(cleaned_df, "data/processed/cleaned_sales.csv")

# Update SQLite with cleaned data
db.save_dataframe(cleaned_df, table_name)
db.verify_row_count(table_name)

# Create Analyzer
analyzer = Analyzer(db, cleaned_df)
# print(f"Total Sales         : {analyzer.total_sales():,.2f}")
# print(f"Total Profit        : {analyzer.total_profit():,.2f}")
# print(f"Profit Margin       : {analyzer.profit_margin():.2f}%")
# print(f"Total Orders        : {analyzer.total_orders()}")
# print(f"Average Order Value : {analyzer.average_order_value():,.2f}")
# print(f"Total Customers     : {analyzer.total_customers()}")

# print(f"Top Category        : {analyzer.top_category()}")
# print(f"Top Sub-Category    : {analyzer.top_sub_category()}")
# print(f"Top Region          : {analyzer.top_region()}")
# print(f"Worst Region        : {analyzer.worst_region()}")
# print(f"Worst State           : {analyzer.worst_state()}")

# print("\nMonthly Sales Trend")
# print(analyzer.monthly_sales())
# print("\nMonthly Profit Trend")
# print(analyzer.monthly_profit())
# print("\nSales by Category")
# print(analyzer.sales_by_category())
# print("\nSales by Region")
# print(analyzer.sales_by_region())
# print("\nSales by Segment")
# print(analyzer.sales_by_segment())
# print("\nTop 10 Products")
# print(analyzer.top_products())
# print("\nTop 10 Customers")
# print(analyzer.top_customers())
kpis = analyzer.kpi_summary()

print("\n========== KPI SUMMARY ==========\n")
for key, value in kpis.items():
    print(f"\n{key.upper()}")
    print(value)
db.close()
