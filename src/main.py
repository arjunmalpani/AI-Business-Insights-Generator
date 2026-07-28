from data_loader import DataLoader
from database import Database

loader = DataLoader("data/raw/sales.csv")

df = loader.load_data()
loader.show_summary(df)
loader.preview_data(df)

db = Database("data/analytics.db")
db2 = Database("data/analytics.db")
db.connect()
table_name = "sales"
# add the df to sql db
db.save_dataframe(df, table_name)
db.verify_row_count(table_name)
db.close()
