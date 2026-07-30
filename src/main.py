import json
from data_loader import DataLoader
from database import Database
from cleaner import Cleaner
from analyzer import Analyzer
from visulization import Visualizer
from ai_insights import AIInsights
from report_generator import ReportGenerator

# Initialize data loader and database connection objects
loader = DataLoader("data/raw/sales.csv")
db = Database("data/analytics.db")

# Load raw sales data into a DataFrame
df = loader.load_data()

# # Show original dataset
# loader.show_summary(df)
# loader.preview_data(df)

# Connect to SQLite database
db.connect()

table_name = "sales"

# Persist raw data to the database for backup and audit purposes
db.save_dataframe(df, table_name)
# db.verify_row_count(table_name)

# Clean data using the Cleaner utility
cleaner = Cleaner()
cleaned_df = cleaner.clean_data(df)

# Validate the cleaned data before further processing
cleaner.validate_data(cleaned_df)

# Show summary and preview of cleaned data for quick inspection
loader.show_summary(cleaned_df)
loader.preview_data(cleaned_df)

# Save cleaned data to a processed CSV file
cleaner.save_cleaned_data(cleaned_df, "data/processed/cleaned_sales.csv")

# Update the database with cleaned records and verify row count
db.save_dataframe(cleaned_df, table_name)
db.verify_row_count(table_name)

# Create an Analyzer instance to compute business metrics
analyzer = Analyzer(db, cleaned_df)

# Generate KPI summary from the cleaned data
kpis = analyzer.kpi_summary()

print("\nKPI SUMMARY n")
for key, value in kpis.items():
    print(f"\n{key.upper()}")
    print(value)

# Visualization: generate data frames for various plots
visualizer = Visualizer()
monthly_sales_df = analyzer.monthly_sales()
monthly_profit_df = analyzer.monthly_profit()
sales_by_category_df = analyzer.sales_by_category()
sales_by_region_df = analyzer.sales_by_region()
sales_by_segment_df = analyzer.sales_by_segment()
top_products_df = analyzer.top_products()

# Render visualizations to help interpret the data
visualizer.plot_monthly_sales(monthly_sales_df)
visualizer.plot_monthly_profit(monthly_profit_df)
visualizer.plot_sales_by_category(sales_by_category_df)
visualizer.plot_sales_by_region(sales_by_region_df)
visualizer.plot_sales_by_segment(sales_by_segment_df)
visualizer.plot_top_products(top_products_df)
visualizer.plot_profit_distribution(cleaned_df)

# ------------- AI Insights
# Convert KPI summary to JSON before sending it to the AI insights generator
ai = AIInsights()
formatted_kpis = json.dumps(kpis, indent=4, default=str)
insights = ai.generate_insights(formatted_kpis)

# Generate the final HTML report using KPIs and AI-generated insights
report = ReportGenerator()
report.generate_html(kpis, insights)
db.close()  # Close database connection once all work is finished
