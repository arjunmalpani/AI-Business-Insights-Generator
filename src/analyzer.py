class Analyzer:

    def __init__(self, db, df):
        self.db = db
        self.df = df

    # ----------- SQL KPIs -------------
    def total_sales(self):
        query = """
        SELECT SUM(sales)
        FROM sales;
        """
        return self.db.execute_query(query)

    def total_profit(self):
        query = """
        SELECT SUM(profit)
        FROM sales;
        """
        return self.db.execute_query(query)

    def total_orders(self):
        query = """
        SELECT COUNT(DISTINCT order_id)
        FROM sales;
        """
        return self.db.execute_query(query)

    def total_customers(self):
        query = """
        SELECT COUNT(DISTINCT customer_id)
        FROM sales;
        """
        return self.db.execute_query(query)

    def profit_margin(self):
        query = """
        SELECT ROUND((SUM(profit) * 100.0) / SUM(sales), 2)
        FROM sales;        """
        return self.db.execute_query(query)

    def average_order_value(self):
        query = """
        SELECT SUM(sales) / COUNT(DISTINCT order_id)
        FROM sales;
        """
        return self.db.execute_query(query)

    def top_category(self):
        query = """
        SELECT category, SUM(sales) as total_sales 
        FROM sales
        GROUP BY category
        ORDER BY total_sales DESC
        LIMIT 1
        """
        return self.db.execute_query(query)

    def top_sub_category(self):
        query = """
        SELECT sub_category, SUM(sales) as total_sales 
        FROM sales
        GROUP BY sub_category
        ORDER BY total_sales DESC
        LIMIT 1
        """
        return self.db.execute_query(query)

    def top_region(self):
        query = """
        SELECT region, SUM(sales) as total_sales 
        FROM sales
        GROUP BY region
        ORDER BY total_sales DESC
        LIMIT 1
        """
        return self.db.execute_query(query)

    def top_state(self):
        query = """
        SELECT state, SUM(sales) as total_sales 
        FROM sales
        GROUP BY state
        ORDER BY total_sales DESC
        LIMIT 1
        """
        return self.db.execute_query(query)

    def worst_region(self):
        query = """
        SELECT region, SUM(sales) as total_sales 
        FROM sales
        GROUP BY region
        ORDER BY total_sales ASC
        LIMIT 1
        """
        return self.db.execute_query(query)

    def worst_state(self):
        query = """
        SELECT state, SUM(sales) as total_sales 
        FROM sales
        GROUP BY state
        ORDER BY total_sales ASC
        LIMIT 1
        """
        return self.db.execute_query(query)

    # -------------- Pandas KPIs -------------
    def monthly_sales(self):
        monthly_sales = (
            self.df.groupby(self.df["order_date"].dt.to_period("M"))["sales"]
            .sum()
            .reset_index()
        )
        monthly_sales["order_date"] = monthly_sales["order_date"].astype("str")
        return monthly_sales

    def monthly_profit(self):
        monthly_profit = (
            self.df.groupby(self.df["order_date"].dt.to_period("M"))["profit"]
            .sum()
            .reset_index()
        )
        monthly_profit["order_date"] = monthly_profit["order_date"].astype("str")
        return monthly_profit

    def sales_by_category(self):
        sales_by_category = (
            self.df.groupby("category")["sales"]
            .sum()
            .sort_values(ascending=False)
            .reset_index()
        )
        return sales_by_category

    def sales_by_region(self):
        sales_by_region = (
            self.df.groupby("region")["sales"]
            .sum()
            .sort_values(ascending=False)
            .reset_index()
        )
        return sales_by_region

    def sales_by_segment(self):
        sales_by_segment = (
            self.df.groupby("segment")["sales"]
            .sum()
            .sort_values(ascending=False)
            .reset_index()
        )
        return sales_by_segment

    def top_products(self):
        top_products = (
            self.df.groupby("product_name")["sales"]
            .sum()
            .sort_values(ascending=False)
            .head(10)
            .reset_index()
        )
        return top_products

    def top_customers(self):
        top_customers = (
            self.df.groupby("customer_name")["sales"]
            .sum()
            .sort_values(ascending=False)
            .head(10)
            .reset_index()
        )
        return top_customers

    # KPI summary
    def kpi_summary(self):
        return {
            # ---------- SQL KPIs ----------
            "total_sales": self.total_sales(),
            "total_profit": self.total_profit(),
            "profit_margin": self.profit_margin(),
            "total_orders": self.total_orders(),
            "total_customers": self.total_customers(),
            "average_order_value": self.average_order_value(),
            "top_category": self.top_category(),
            "top_sub_category": self.top_sub_category(),
            "top_region": self.top_region(),
            "top_state": self.top_state(),
            "worst_region": self.worst_region(),
            "worst_state": self.worst_state(),
            # ---------- Pandas KPIs ----------
            "monthly_sales": self.monthly_sales(),
            "monthly_profit": self.monthly_profit(),
            "sales_by_category": self.sales_by_category(),
            "sales_by_region": self.sales_by_region(),
            "sales_by_segment": self.sales_by_segment(),
            "top_products": self.top_products(),
            "top_customers": self.top_customers(),
        }
