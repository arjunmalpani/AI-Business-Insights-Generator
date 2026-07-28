from data_loader import DataLoader
from database import Database
from cleaner import Cleaner

# Load data
loader = DataLoader("data/raw/sales.csv")
df = loader.load_data()

# Show original dataset
loader.show_summary(df)
loader.preview_data(df)

# Database
db = Database("data/analytics.db")
db.connect()

table_name = "sales"

# Save raw data
db.save_dataframe(df, table_name)
db.verify_row_count(table_name)

# Clean data
cleaner = Cleaner()
cleaned_df = cleaner.clean_data(df)

# Validate cleaned data
cleaner.validate_data(cleaned_df)

# Save cleaned CSV
cleaner.save_cleaned_data(cleaned_df, "data/processed/cleaned_sales.csv")

# Update SQLite with cleaned data
db.save_dataframe(cleaned_df, table_name)
db.verify_row_count(table_name)

db.close()
