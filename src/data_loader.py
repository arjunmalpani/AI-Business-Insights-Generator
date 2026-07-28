import pandas as pd


class DataLoader:

    def __init__(self, csv_path):
        self.csv_path = csv_path

    def load_data(self):
        try:
            df = pd.read_csv(self.csv_path)
            print("CSV loaded Successfully")
            return df
        except FileNotFoundError:
            print(f"File not found: {self.csv_path}")
            raise
        except pd.errors.EmptyDataError:
            print(f"CSV is Empty")
            raise
        except pd.errors.ParserError:
            print(f"Invalid CSV Format")
            raise
        except Exception as e:
            print(f"Unexpected Error {e}")
            raise

    def show_summary(self, df):
        row_size, columns_size = df.shape
        missing_values = df.isnull().sum().sum()
        duplicate_rows_value = df.duplicated().sum()
        columns_names = df.columns
        data_types = df.dtypes
        memory_usage = df.memory_usage(deep=True).sum() / 1024**2
        print("Dataset Summary")
        print("-" * 30)
        print(f"Rows: {row_size}")
        print(f"Columns: {columns_size}")
        print(f"Missing Values: {missing_values}")
        print(f"Duplicate Values: {duplicate_rows_value}")
        print("Columns Names:")
        for i, col in enumerate(columns_names, start=1):
            print(f"{i}. {col}")
        print("Data Types:")
        print(data_types)
        print(f"Memory Usage: {memory_usage:.2f} MB")

    def preview_data(self, df):
        # display first 5 rows
        print("-" * 30)
        print("FIRST 5 ROWS")
        print("-" * 30)
        print(df.head())
        print("-" * 30)
        print("LAST 5 ROWS")
        print("-" * 30)
        # display last 5 rows
        print(df.tail())
