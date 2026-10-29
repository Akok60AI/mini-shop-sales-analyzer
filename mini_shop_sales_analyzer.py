
import io
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import gradio as gr


def analyze_sales(manual_text, uploaded_file):
    try:
        if uploaded_file:
            path = (
                uploaded_file
                if isinstance(uploaded_file, str)
                else uploaded_file.name
            )

            if path.lower().endswith(".csv"):
                data = pd.read_csv(path)
            elif path.lower().endswith((".xlsx", ".xls")):
                data = pd.read_excel(path)
            else:
                raise ValueError("Upload a CSV or Excel file.")
        else:
            if not manual_text or not manual_text.strip():
                raise ValueError("Enter sales or upload a file.")

            data = pd.read_csv(
                io.StringIO(manual_text),
                header=None,
                names=["Product", "Quantity", "Price"],
                skipinitialspace=True
            )
            data["Quantity"] = pd.to_numeric(
                data["Quantity"], errors="coerce"
            )
            data["Price"] = pd.to_numeric(
                data["Price"], errors="coerce"
            )
            data = data.dropna(subset=["Quantity", "Price"])

        data.columns = [str(c).strip().lower() for c in data.columns]
        required = {"product", "quantity", "price"}

        if not required.issubset(data.columns):
            raise ValueError(
                "Required columns: Product, Quantity, Price."
            )

        data = data[["product", "quantity", "price"]].copy()
        data["product"] = data["product"].astype("string").str.strip()
        data["quantity"] = pd.to_numeric(
            data["quantity"], errors="coerce"
        )
        data["price"] = pd.to_numeric(
            data["price"], errors="coerce"
        )
        data = data.dropna(subset=["product", "quantity", "price"])
        data = data[data["product"] != ""]

        if data.empty:
            raise ValueError("No valid sales rows found.")
        if (data["quantity"] <= 0).any():
            raise ValueError("Quantities must be greater than zero.")
        if (data["price"] < 0).any():
            raise ValueError("Prices cannot be negative.")

        data["Total Sales"] = data["quantity"] * data["price"]
        data = data.rename(columns={
            "product": "Product",
            "quantity": "Quantity",
            "price": "Price"
        })

        by_quantity = data.groupby("Product")["Quantity"].sum()
        by_revenue = data.groupby("Product")["Total Sales"].sum()

        summary = (
            "# Mini Shop Sales Report\n\n"
            f"**Total items sold:** {data['Quantity'].sum():g}\n\n"
            f"**Total revenue:** {data['Total Sales'].sum():,.2f}\n\n"
            f"**Best-selling product:** {by_quantity.idxmax()}\n\n"
            "## Revenue by product\n\n"
            + by_revenue.to_string()
        )

        fig, ax = plt.subplots(figsize=(8, 4))
        by_revenue.sort_values(ascending=False).plot(
            kind="bar", ax=ax
        )
        ax.set_title("Revenue by Product")
        ax.set_xlabel("Product")
        ax.set_ylabel("Revenue")
        ax.tick_params(axis="x", rotation=30)
        fig.tight_layout()

        return data, summary, fig

    except Exception as error:
        return pd.DataFrame(), f"**Please check your data:** {error}", None


with gr.Blocks(title="Mini Shop Sales Analyzer") as app:
    gr.Markdown(
        "# Mini Shop Sales Analyzer\n"
        "Enter sales manually or upload a CSV/Excel file.\n\n"
        "Manual format: one product per line as "
        "`Product,Quantity,Price`."
    )

    manual = gr.Textbox(
        label="Manual sales entry",
        value="Bread,10,2\nMilk,5,3\nRice,3,10",
        lines=5
    )

    upload = gr.File(
        label="Upload CSV or Excel",
        file_types=[".csv", ".xlsx", ".xls"],
        type="filepath"
    )

    button = gr.Button("Analyze Sales", variant="primary")
    table = gr.Dataframe(label="Sales Details")
    report = gr.Markdown()
    chart = gr.Plot(label="Revenue Chart")

    button.click(
        analyze_sales,
        inputs=[manual, upload],
        outputs=[table, report, chart]
    )

app.launch()


