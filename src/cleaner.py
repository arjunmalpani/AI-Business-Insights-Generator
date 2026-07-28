import pandas as pd


class Cleaner:
    def clean_data(self, df):
        # handle duplicate values
        cleaned_df = df.copy()
        before_len = len(cleaned_df)
        cleaned_df = cleaned_df.drop_duplicates()
        print(f"Removed {before_len - len(cleaned_df)} duplicate rows.")

        # handle missing values
        # Numeric columns - fill with median
        # Text columns - fill with "Unknown"
        numeric_columns = cleaned_df.select_dtypes(include="number").columns
        text_columns = cleaned_df.select_dtypes(include=["string", "object"]).columns
        for column in numeric_columns:
            cleaned_df[column] = cleaned_df[column].fillna(cleaned_df[column].median())
        for column in text_columns:
            cleaned_df[column] = cleaned_df[column].fillna("Unknown")

        # remove extra whitespace
        text_columns = cleaned_df.select_dtypes(include=["object", "string"]).columns

        for column in text_columns:
            cleaned_df[column] = cleaned_df[column].str.strip()

        # standardization columns names
        cleaned_df.columns = (
            cleaned_df.columns.str.strip().str.lower().str.replace(" ", "_")
        )
        # datatime
        date_columns = ["order_date", "ship_date"]
        for column in date_columns:
            cleaned_df[column] = pd.to_datetime(cleaned_df[column], errors="coerce")
        # handle numeric data
        numeric_columns = cleaned_df.select_dtypes(include=["number"]).columns

        for column in numeric_columns:
            cleaned_df[column] = pd.to_numeric(cleaned_df[column], errors="coerce")

        print("Numeric columns converted.")

        return cleaned_df

    def validate_data(self, df):
        print("\nValidation Report")
        print("-" * 30)
        print(f"Rows: {len(df)}")
        print(f"Missing Values: {df.isnull().sum().sum()}")
        print(f"Duplicate Rows: {df.duplicated().sum()}")

    def save_cleaned_data(self, df, output_path):
        df.to_csv(output_path, index=False)
        print(f"Saved cleaned data to {output_path}")
