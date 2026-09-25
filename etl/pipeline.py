from pathlib import Path
import sqlite3
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
RAW_FILE = DATA_DIR / "raw_sales.csv"
CLEAN_FILE = DATA_DIR / "cleaned_sales.csv"
DB_FILE = ROOT / "sales.db"

SEED = 42
N_ROWS = 20_000

PRODUCTS = {
    "Electronics": {
        "Wireless Headphones": 80, "Smartphone": 650, "Laptop": 900,
        "Smartwatch": 180, "Bluetooth Speaker": 70
    },
    "Home & Kitchen": {
        "Air Fryer": 120, "Coffee Maker": 90, "Cookware Set": 150,
        "Vacuum Cleaner": 220, "Table Lamp": 45
    },
    "Clothing": {
        "T-Shirt": 25, "Jeans": 60, "Sneakers": 85,
        "Jacket": 110, "Backpack": 55
    },
    "Sports": {
        "Yoga Mat": 30, "Running Shoes": 95, "Dumbbells": 70,
        "Football": 35, "Tennis Racket": 100
    },
    "Books": {
        "Fiction Book": 18, "Business Book": 28, "Python Book": 35,
        "Data Science Book": 42, "Self Help Book": 22
    }
}

COUNTRIES = {
    "North": ["India"], "South": ["India"], "East": ["India"],
    "West": ["India"], "Central": ["India"]
}
PAYMENTS = ["Credit Card", "UPI", "Debit Card", "Net Banking", "Wallet"]
REGIONS = list(COUNTRIES)
CATEGORIES = list(PRODUCTS)


def generate_raw_data(n=N_ROWS, seed=SEED):
    rng = np.random.default_rng(seed)
    dates = pd.date_range(end=pd.Timestamp.today().normalize(), periods=730, freq="D")

    category_weights = [0.28, 0.22, 0.23, 0.15, 0.12]
    category = rng.choice(CATEGORIES, n, p=category_weights)
    region = rng.choice(REGIONS, n, p=[0.24, 0.23, 0.18, 0.20, 0.15])

    products = []
    prices = []
    for c in category:
        names = list(PRODUCTS[c])
        product = rng.choice(names)
        products.append(product)
        prices.append(PRODUCTS[c][product] * rng.uniform(0.85, 1.15))

    base_qty = rng.choice([1, 2, 3, 4, 5], n, p=[0.43, 0.30, 0.15, 0.08, 0.04])
    discounts = np.clip(rng.normal(0.10, 0.055, n), 0, 0.30)

    customer_num = rng.integers(1, 3501, n)
    customer_names = [f"Customer {i}" for i in customer_num]

    df = pd.DataFrame({
        "order_id": np.arange(100001, 100001 + n),
        "order_date": rng.choice(dates, n),
        "customer_id": [f"C{i:05d}" for i in customer_num],
        "customer_name": customer_names,
        "region": region,
        "country": [COUNTRIES[r][0] for r in region],
        "category": category,
        "product": products,
        "quantity": base_qty,
        "unit_price": np.round(prices, 2),
        "discount": np.round(discounts, 3),
        "payment_method": rng.choice(PAYMENTS, n, p=[0.28, 0.32, 0.18, 0.12, 0.10])
    })

    # A few realistic data-quality issues for the ETL to demonstrate handling.
    duplicate_rows = df.sample(100, random_state=seed)
    df = pd.concat([df, duplicate_rows], ignore_index=True)
    missing_idx = rng.choice(df.index, 80, replace=False)
    df.loc[missing_idx[:40], "region"] = np.nan
    df.loc[missing_idx[40:], "payment_method"] = np.nan
    return df


def clean_and_transform(df):
    raw_count = len(df)
    duplicate_count = int(df.duplicated(subset=["order_id"]).sum())
    df = df.drop_duplicates(subset=["order_id"]).copy()

    before_missing = int(df.isna().sum().sum())
    df["region"] = df["region"].fillna("Central")
    df["payment_method"] = df["payment_method"].fillna("UPI")
    df["country"] = df["country"].fillna("India")
    df["customer_name"] = df["customer_name"].fillna("Unknown Customer")

    df["order_date"] = pd.to_datetime(df["order_date"], errors="coerce")
    df["quantity"] = pd.to_numeric(df["quantity"], errors="coerce").fillna(1).clip(lower=1)
    df["unit_price"] = pd.to_numeric(df["unit_price"], errors="coerce").fillna(1).clip(lower=0)
    df["discount"] = pd.to_numeric(df["discount"], errors="coerce").fillna(0).clip(0, 0.30)

    df["category"] = df["category"].astype(str).str.strip().str.title()
    df["region"] = df["region"].astype(str).str.strip().str.title()

    df["gross_sales"] = df["quantity"] * df["unit_price"]
    df["discount_amount"] = df["gross_sales"] * df["discount"]
    df["revenue"] = df["gross_sales"] - df["discount_amount"]

    # Category-specific cost ratios create realistic differences in margins.
    cost_rates = {
        "Electronics": 0.72, "Home & Kitchen": 0.65, "Clothing": 0.55,
        "Sports": 0.58, "Books": 0.62
    }
    df["estimated_cost"] = df["revenue"] * df["category"].map(cost_rates).fillna(0.65)
    df["profit"] = df["revenue"] - df["estimated_cost"]
    df["profit_margin"] = np.where(df["revenue"] > 0, df["profit"] / df["revenue"], 0)

    df["order_month"] = df["order_date"].dt.month
    df["order_year"] = df["order_date"].dt.year
    df["order_year_month"] = df["order_date"].dt.to_period("M").astype(str)

    numeric_cols = ["quantity", "unit_price", "discount", "gross_sales",
                    "discount_amount", "revenue", "estimated_cost", "profit", "profit_margin"]
    df[numeric_cols] = df[numeric_cols].round(4)
    df = df.sort_values("order_date").reset_index(drop=True)

    missing_handled = max(0, before_missing - int(df.isna().sum().sum()))
    return df, raw_count, duplicate_count, missing_handled


def load_to_sqlite(df):
    with sqlite3.connect(DB_FILE) as conn:
        df.to_sql("sales", conn, if_exists="replace", index=False)
        conn.execute("CREATE INDEX IF NOT EXISTS idx_sales_date ON sales(order_date)")
        conn.execute("CREATE INDEX IF NOT EXISTS idx_sales_category ON sales(category)")
        conn.execute("CREATE INDEX IF NOT EXISTS idx_sales_region ON sales(region)")
        conn.commit()


def run_pipeline():
    DATA_DIR.mkdir(exist_ok=True)
    if not RAW_FILE.exists():
        raw = generate_raw_data()
        raw.to_csv(RAW_FILE, index=False)
    else:
        raw = pd.read_csv(RAW_FILE)

    cleaned, raw_count, duplicate_count, missing_handled = clean_and_transform(raw)
    cleaned.to_csv(CLEAN_FILE, index=False)
    load_to_sqlite(cleaned)

    print(f"Number of raw records: {raw_count}")
    print(f"Number of cleaned records: {len(cleaned)}")
    print(f"Number of duplicates removed: {duplicate_count}")
    print(f"Number of missing values handled: {missing_handled}")
    print(f"Total revenue: ₹{cleaned['revenue'].sum():,.2f}")
    print(f"Total profit: ₹{cleaned['profit'].sum():,.2f}")
    print("Pipeline completed successfully.")


if __name__ == "__main__":
    run_pipeline()
