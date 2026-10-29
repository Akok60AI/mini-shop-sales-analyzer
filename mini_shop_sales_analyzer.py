
# Mini Shop Sales Analyzer

import pandas as pd

sales = {
    "Product": ["Bread", "Milk", "Rice", "Bread", "Milk", "Rice"],
    "Quantity": [10, 5, 3, 8, 7, 4],
    "Price": [2, 3, 10, 2, 3, 10]
}

df = pd.DataFrame(sales)
df["Total Sales"] = df["Quantity"] * df["Price"]

print("MINI SHOP SALES ANALYZER")
print("------------------------")
print(df)

print("\nTotal Revenue:", df["Total Sales"].sum())
print("Best-Selling Product:")
print(df.groupby("Product")["Quantity"].sum().idxmax())
