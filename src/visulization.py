import matplotlib.pyplot as plt


class Visualizer:
    def __init__(self):
        pass

    def plot_monthly_sales(self, monthly_sales):
        plt.figure(figsize=(12, 6))

        plt.plot(monthly_sales["order_date"], monthly_sales["sales"], marker="o")

        plt.title("Monthly Sales Trend")
        plt.xlabel("Month")
        plt.ylabel("Sales")

        plt.xticks(rotation=45)

        plt.tight_layout()

        plt.savefig("charts/monthly_sales.png")

        plt.close()

    def plot_monthly_profit(self, monthly_profit):
        plt.figure(figsize=(12, 6))

        plt.plot(monthly_profit["order_date"], monthly_profit["profit"], marker="o")

        plt.title("Monthly Profit Trend")
        plt.xlabel("Month")
        plt.ylabel("Profit")

        plt.xticks(rotation=45)

        plt.tight_layout()

        plt.savefig("charts/monthly_profit.png")

        plt.close()

    def plot_sales_by_category(self, sales_by_category):
        plt.figure(figsize=(12, 6))

        plt.bar(sales_by_category["category"], sales_by_category["sales"])

        plt.title("Sales by Category")
        plt.xlabel("Category")
        plt.ylabel("Sales")

        plt.xticks(rotation=45)

        plt.tight_layout()

        plt.savefig("charts/sales_by_category.png")

        plt.close()

    def plot_sales_by_region(self, sales_by_region):
        plt.figure(figsize=(12, 6))

        plt.bar(sales_by_region["region"], sales_by_region["sales"])

        plt.title("Sales by Region")
        plt.xlabel("Region")
        plt.ylabel("Sales")

        plt.xticks(rotation=45)

        plt.tight_layout()

        plt.savefig("charts/sales_by_region.png")

        plt.close()

    def plot_sales_by_segment(self, sales_by_segment):
        plt.figure(figsize=(8, 8))

        plt.pie(
            sales_by_segment["sales"],
            labels=sales_by_segment["segment"],
            autopct="%1.1f%%",
            startangle=90,
        )

        plt.title("Sales by Segment")

        plt.tight_layout()

        plt.savefig("charts/sales_by_segment.png")

        plt.close()

    def plot_top_products(self, top_products):
        plt.figure(figsize=(12, 6))

        plt.barh(top_products["product_name"], top_products["sales"])  # barh(y,data)

        plt.title("Top 10 Products")
        plt.xlabel("Sales")
        plt.ylabel("Product Name")

        plt.xticks(rotation=45)

        plt.tight_layout()

        plt.savefig("charts/top_products.png")

        plt.close()

    def plot_profit_distribution(self, df):
        plt.figure(figsize=(10, 6))

        lower = df["profit"].quantile(0.01)
        upper = df["profit"].quantile(0.99)

        plt.hist(df["profit"], bins=100)
        plt.xlim(lower, upper)

        plt.title("Profit Distribution")
        plt.xlabel("Profit")
        plt.ylabel("Number of Orders")

        plt.tight_layout()

        plt.savefig("charts/profit_distribution.png")

        plt.close()
