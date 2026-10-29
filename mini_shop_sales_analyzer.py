
# Mini Shop Sales Analyzer
# A simple Python project for analyzing shop sales

import pandas as pd
import matplotlib.pyplot as plt

# 1. Shop sales data
sales = {
    "Product": ["Bread", "Milk", "Rice", "Bread", "Milk", "Rice"],
    "Quantity": [10, 5, 3, 8, 7, 4],
    "Price": [2, 3, 10, 2, 3, 10]
}

df = pd.DataFrame(sales)
df["Total Sales"] = df["Quantity"] * df["Price"]

# 2. Sales report
print("=" * 35)
print("       MINI SHOP SALES REPORT")
print("=" * 35)
print(df.to_string(index=False))

# 3. Total revenue
print("\nTotal Revenue:", df["Total Sales"].sum())

# 4. Quantity sold by product
print("\nQuantity Sold by Product:")
print(df.groupby("Product")["Quantity"].sum())

# 5. Best-selling product
best_seller = df.groupby("Product")["Quantity"].sum().idxmax()
print("\nBest-Selling Product:", best_seller)

# 6. Revenue by product
revenue = df.groupby("Product")["Total Sales"].sum()
print("\nRevenue by Product:")
print(revenue)

# 7. Sales chart
revenue.plot(kind="bar")
plt.title("Revenue by Product")
plt.xlabel("Product")
plt.ylabel("Total Sales")
plt.xticks(rotation=0)
plt.tight_layout()
plt.show()

