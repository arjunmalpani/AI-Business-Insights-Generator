import sqlite3


class Database:
    # database initialization
    def __init__(self, db_path):
        self.db_path = db_path
        self.connection = None

    # database connection
    def connect(self):
        self.connection = sqlite3.connect(self.db_path)
        print(f"Connected to ({self.db_path}) the SQLite Successfully")

    # database disconnection
    def close(self):
        if self.connection:
            self.connection.close()
        print(f"disconnected to ({self.db_path}) the SQLite Successfully")

    # saving data frame
    def save_dataframe(self, df, table_name):
        df.to_sql(table_name, self.connection, if_exists="replace", index=False)

    # verify row count
    def verify_row_count(self, table_name):
        cursor = self.connection.cursor()
        cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
        row_count = cursor.fetchone()[0]
        print(f"Rows in '{table_name}': {row_count}")

    def execute_query(self, query):
        cursor = self.connection.cursor()
        cursor.execute(query)
        return cursor.fetchone()[0]
