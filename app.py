from pathlib import Path
import sqlite3
import subprocess
import sys

import pandas as pd
import plotly.express as px
import streamlit as st

ROOT = Path(__file__).resolve().parent
DB_FILE = ROOT / "sales.db"
CLEAN_FILE = ROOT / "data" / "cleaned_sales.csv"
PIPELINE = ROOT / "etl" / "pipeline.py"

st.set_page_config(
    page_title="E-Commerce Sales Intelligence",
    page_icon="📊",
    layout="wide",
)

@st.cache_data
def ensure_data():
    if not CLEAN_FILE.exists() or not DB_FILE.exists():
        result = subprocess.run(
            [sys.executable, str(PIPELINE)],
            cwd=ROOT,
            capture_output=True,
            text=True,
        )
        if result.returncode != 0:
            raise RuntimeError(result.stderr or "ETL pipeline failed.")
    with sqlite3.connect(DB_FILE) as conn:
        df = pd.read_sql_query("SELECT * FROM sales", conn)
    df["order_date"] = pd.to_datetime(df["order_date"], errors="coerce")
    return df

def money(x):
    return f"₹{x:,.0f}"

def safe_div(a, b):
    return a / b if b else 0

try:
    df = ensure_data()
except Exception as e:
    st.error(f"Could not prepare the data: {e}")
    st.stop()

st.title("📊 E-Commerce Sales Intelligence Platform")
st.caption("End-to-end Data Engineering + Data Analytics portfolio project")

# Sidebar filters
st.sidebar.header("Filters")
min_date = df["order_date"].min().date()
max_date = df["order_date"].max().date()
date_range = st.sidebar.date_input("Date range", (min_date, max_date), min_value=min_date, max_value=max_date)

if isinstance(date_range, tuple) and len(date_range) == 2:
    start_date, end_date = date_range
else:
    start_date, end_date = min_date, max_date

regions = sorted(df["region"].dropna().unique())
categories = sorted(df["category"].dropna().unique())
products = sorted(df["product"].dropna().unique())

selected_regions = st.sidebar.multiselect("Region", regions, default=regions)
selected_categories = st.sidebar.multiselect("Category", categories, default=categories)
selected_products = st.sidebar.multiselect("Product", products, default=products)

filtered = df[
    (df["order_date"].dt.date >= start_date) &
    (df["order_date"].dt.date <= end_date) &
    (df["region"].isin(selected_regions)) &
    (df["category"].isin(selected_categories)) &
    (df["product"].isin(selected_products))
].copy()

if filtered.empty:
    st.warning("No transactions match the selected filters. Try widening the filters.")
    st.stop()

page = st.sidebar.radio(
    "Navigate",
    ["Executive Overview", "Product Analytics", "Customer Analytics", "Data Explorer"]
)

# KPIs
total_revenue = filtered["revenue"].sum()
total_profit = filtered["profit"].sum()
total_orders = filtered["order_id"].nunique()
total_customers = filtered["customer_id"].nunique()
aov = safe_div(total_revenue, total_orders)
margin = safe_div(total_profit, total_revenue)

def show_kpis():
    cols = st.columns(6)
    values = [
        ("Total Revenue", money(total_revenue)),
        ("Total Profit", money(total_profit)),
        ("Total Orders", f"{total_orders:,}"),
        ("Total Customers", f"{total_customers:,}"),
        ("Average Order Value", money(aov)),
        ("Profit Margin", f"{margin:.1%}"),
    ]
    for col, (label, value) in zip(cols, values):
        col.metric(label, value)

def business_insights():
    st.subheader("💡 Key Business Insights")
    category_rev = filtered.groupby("category")["revenue"].sum()
    region_rev = filtered.groupby("region")["revenue"].sum()
    category_profit = filtered.groupby("category")["profit"].sum()
    product_qty = filtered.groupby("product")["quantity"].sum()
    customer_rev = filtered.groupby(["customer_id", "customer_name"])["revenue"].sum()
    monthly = filtered.groupby("order_year_month")["revenue"].sum()

    highest_cat = category_rev.idxmax()
    highest_region = region_rev.idxmax()
    profitable_cat = category_profit.idxmax()
    best_product = product_qty.idxmax()
    best_customer = customer_rev.idxmax()[1]
    best_month = monthly.idxmax()

    st.info(
        f"**Highest revenue category:** {highest_cat}  \n"
        f"**Highest revenue region:** {highest_region}  \n"
        f"**Most profitable category:** {profitable_cat}  \n"
        f"**Best-selling product:** {best_product}  \n"
        f"**Highest-value customer:** {best_customer}  \n"
        f"**Best-performing month:** {best_month}"
    )

if page == "Executive Overview":
    show_kpis()
    st.divider()

    st.subheader("Revenue Over Time")
    monthly = filtered.groupby("order_year_month", as_index=False).agg(
        revenue=("revenue", "sum")
    )
    fig = px.line(monthly, x="order_year_month", y="revenue", markers=True)
    fig.update_layout(xaxis_title="Month", yaxis_title="Revenue (₹)")
    st.plotly_chart(fig, use_container_width=True)

    c1, c2 = st.columns(2)
    with c1:
        st.subheader("Revenue by Category")
        d = filtered.groupby("category", as_index=False)["revenue"].sum().sort_values("revenue", ascending=False)
        st.plotly_chart(px.bar(d, x="category", y="revenue"), use_container_width=True)
    with c2:
        st.subheader("Revenue by Region")
        d = filtered.groupby("region", as_index=False)["revenue"].sum().sort_values("revenue", ascending=False)
        st.plotly_chart(px.bar(d, x="region", y="revenue"), use_container_width=True)

    c1, c2 = st.columns(2)
    with c1:
        st.subheader("Profit by Category")
        d = filtered.groupby("category", as_index=False)["profit"].sum().sort_values("profit", ascending=False)
        st.plotly_chart(px.bar(d, x="category", y="profit"), use_container_width=True)
    with c2:
        st.subheader("Monthly Order Trend")
        d = filtered.groupby("order_year_month", as_index=False).agg(orders=("order_id", "nunique"))
        st.plotly_chart(px.line(d, x="order_year_month", y="orders", markers=True), use_container_width=True)

    st.subheader("Top 10 Products by Revenue")
    top = filtered.groupby("product", as_index=False)["revenue"].sum().sort_values("revenue", ascending=False).head(10)
    st.dataframe(top, use_container_width=True, hide_index=True)
    business_insights()

elif page == "Product Analytics":
    show_kpis()
    st.divider()
    c1, c2 = st.columns(2)

    with c1:
        st.subheader("Top 10 Products by Revenue")
        d = filtered.groupby("product", as_index=False)["revenue"].sum().nlargest(10, "revenue")
        st.plotly_chart(px.bar(d, x="revenue", y="product", orientation="h"), use_container_width=True)

    with c2:
        st.subheader("Top 10 Products by Profit")
        d = filtered.groupby("product", as_index=False)["profit"].sum().nlargest(10, "profit")
        st.plotly_chart(px.bar(d, x="profit", y="product", orientation="h"), use_container_width=True)

    c1, c2 = st.columns(2)
    with c1:
        d = filtered.groupby("category", as_index=False)["revenue"].sum()
        st.subheader("Revenue by Category")
        st.plotly_chart(px.pie(d, names="category", values="revenue"), use_container_width=True)
    with c2:
        d = filtered.groupby("category", as_index=False)["profit"].sum()
        st.subheader("Profit by Category")
        st.plotly_chart(px.bar(d, x="category", y="profit"), use_container_width=True)

    d = filtered.groupby("category", as_index=False)["quantity"].sum()
    st.subheader("Quantity Sold by Category")
    st.plotly_chart(px.bar(d, x="category", y="quantity"), use_container_width=True)

elif page == "Customer Analytics":
    show_kpis()
    st.divider()
    customer = filtered.groupby(["customer_id", "customer_name"], as_index=False).agg(
        revenue=("revenue", "sum"),
        orders=("order_id", "nunique"),
        profit=("profit", "sum"),
    )
    customer["segment"] = pd.cut(
        customer["revenue"],
        bins=[-float("inf"), customer["revenue"].quantile(0.50), customer["revenue"].quantile(0.80), float("inf")],
        labels=["Low Value", "Medium Value", "High Value"],
        include_lowest=True,
    )

    c1, c2, c3 = st.columns(3)
    c1.metric("Total Customers", f"{len(customer):,}")
    c2.metric("Avg Revenue / Customer", money(customer["revenue"].mean()))
    c3.metric("Avg Orders / Customer", f"{customer['orders'].mean():.2f}")

    st.subheader("Customer Segmentation")
    seg = customer["segment"].value_counts().rename_axis("segment").reset_index(name="customers")
    st.plotly_chart(px.bar(seg, x="segment", y="customers"), use_container_width=True)

    st.subheader("Top 10 Customers")
    top = customer.sort_values("revenue", ascending=False).head(10)
    st.dataframe(top, use_container_width=True, hide_index=True)

else:
    show_kpis()
    st.divider()
    st.subheader("Filtered Transaction Data")
    display_cols = ["order_id", "order_date", "customer_name", "region", "category",
                    "product", "quantity", "revenue", "profit"]
    view = filtered[display_cols].sort_values("order_date", ascending=False)
    st.dataframe(view, use_container_width=True, hide_index=True)

    csv = view.to_csv(index=False).encode("utf-8")
    st.download_button(
        "⬇️ Download filtered CSV",
        data=csv,
        file_name="filtered_sales.csv",
        mime="text/csv",
    )
