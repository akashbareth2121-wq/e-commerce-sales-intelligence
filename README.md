# 📊 E-Commerce Sales Intelligence Platform

> **From raw transactions to business decisions — an end-to-end Data Engineering + Analytics project built with Python, SQL and Streamlit.**

<p align="center">

**🔄 ETL** &nbsp;→&nbsp; **🧹 Data Quality** &nbsp;→&nbsp; **🗄️ SQLite** &nbsp;→&nbsp; **🔎 SQL Analytics** &nbsp;→&nbsp; **📈 Interactive Dashboard** &nbsp;→&nbsp; **💡 Business Insights**

</p>

---

## 🚀 Live Dashboard

🔗 **[ Live Streamlit Dashboard](https://ecommerce-sales-intelligence-fjfdc8yxuulumgb6gxasoi.streamlit.app/)**

> Replace `YOUR_STREAMLIT_APP_URL` with your Streamlit Community Cloud URL after deployment.

---

## 🎯 What is this project?

E-commerce businesses generate thousands of transactions every day, but **raw transaction data alone does not create business value**.

This project demonstrates how raw sales data can be transformed into a reliable analytical dataset and finally into an interactive decision-support dashboard.

The platform simulates an e-commerce business with **20,000+ transactions** across:

- 🛒 5 product categories
- 📦 25 products
- 🌎 5 sales regions
- 👥 3,500+ customers
- 💳 Multiple payment methods
- 📅 Approximately 2 years of transactions

The objective is simple:

> **Turn messy transactional data into clear answers for business stakeholders.**

---

# 🧠 Business Problem

Imagine you are a Data Analyst / Data Engineer working for an e-commerce company.

Management wants answers to questions such as:

- Which category generates the most revenue?
- Which products are the biggest revenue drivers?
- Which category is actually the most profitable?
- Which region performs best?
- Is revenue growing or declining over time?
- Who are the highest-value customers?
- What is the average order value?
- How much discount is being given?
- Which products should receive more attention?

Instead of manually analysing spreadsheets, this project creates a **repeatable data pipeline + analytical database + interactive dashboard** to answer these questions.

---

# 🏗️ Architecture

```text
                 ┌──────────────────────┐
                 │   RAW SALES DATA     │
                 │   raw_sales.csv      │
                 └──────────┬───────────┘
                            │
                            ▼
                 ┌──────────────────────┐
                 │    PYTHON ETL        │
                 │                      │
                 │ Extract              │
                 │ Transform            │
                 │ Validate             │
                 │ Feature Engineering  │
                 │ Load                 │
                 └──────────┬───────────┘
                            │
                  ┌─────────┴─────────┐
                  ▼                   ▼
        ┌─────────────────┐   ┌─────────────────┐
        │ CLEANED CSV     │   │   SQLite DB     │
        │ cleaned_sales   │   │    sales.db     │
        └─────────────────┘   └────────┬────────┘
                                       │
                                       ▼
                              ┌─────────────────┐
                              │  SQL ANALYTICS  │
                              │ analytics.sql   │
                              └────────┬────────┘
                                       │
                                       ▼
                              ┌─────────────────┐
                              │    STREAMLIT    │
                              │    DASHBOARD    │
                              └────────┬────────┘
                                       │
                                       ▼
                         ┌────────────────────────┐
                         │   BUSINESS INSIGHTS    │
                         │                        │
                         │ Revenue • Profit       │
                         │ Products • Customers   │
                         │ Regions • Trends       │
                         └────────────────────────┘
```

---

# ✨ Key Features

### 🔄 Data Engineering

- Reproducible synthetic e-commerce data generation
- 20,000+ transaction records
- Automated ETL pipeline
- Duplicate detection and removal
- Missing-value handling
- Data type validation
- Business-rule validation
- Feature engineering
- SQLite loading

### 📊 Data Analytics

- Revenue analysis
- Profit analysis
- Profit margin analysis
- Average Order Value
- Monthly performance
- Category performance
- Regional performance
- Product performance
- Customer analysis
- Customer segmentation

### 🎨 Interactive Dashboard

- Executive Overview
- Product Analytics
- Customer Analytics
- Data Explorer
- Interactive date filtering
- Region filtering
- Category filtering
- Product filtering
- Interactive Plotly charts
- Dynamic business insights
- Filtered CSV download

---

# 📌 Dashboard

## 1️⃣ Executive Overview

The executive page provides a high-level snapshot of the business.

### KPIs

| KPI | Description |
|---|---|
| 💰 Total Revenue | Total sales revenue after discounts |
| 📈 Total Profit | Estimated profit generated |
| 🛒 Total Orders | Number of unique orders |
| 👥 Total Customers | Number of unique customers |
| 🧾 Average Order Value | Average revenue per order |
| 📊 Profit Margin | Profit as a percentage of revenue |

### Visualizations

- Revenue over time
- Revenue by category
- Revenue by region
- Profit by category
- Monthly order trend
- Top 10 products by revenue

---

# 2️⃣ Product Analytics

Understand which products and categories are driving the business.

### Analysis includes

- 🥇 Top 10 products by revenue
- 💵 Top 10 products by profit
- 📦 Revenue by category
- 📈 Profit by category
- 🛍️ Quantity sold by category

This helps answer:

> **Are the products generating the most sales also generating the most profit?**

---

# 3️⃣ Customer Analytics

The customer page focuses on customer value.

### Metrics

- Total customers
- Average revenue per customer
- Average orders per customer
- Top 10 customers

### Customer Segmentation

Customers are segmented based on their revenue contribution:

```text
                 CUSTOMER VALUE

        ┌─────────────────────────┐
        │       HIGH VALUE        │
        │    Top revenue users    │
        └─────────────────────────┘

        ┌─────────────────────────┐
        │      MEDIUM VALUE       │
        │    Mid-tier customers   │
        └─────────────────────────┘

        ┌─────────────────────────┐
        │       LOW VALUE         │
        │    Lower revenue users  │
        └─────────────────────────┘
```

This gives management a simple way to understand customer concentration.

---

# 4️⃣ Data Explorer

A transaction-level view of the cleaned dataset.

Users can filter by:

- 📅 Date
- 🌎 Region
- 🏷️ Category
- 📦 Product

Displayed fields include:

```text
Order ID
Date
Customer
Region
Category
Product
Quantity
Revenue
Profit
```

The filtered data can also be downloaded as a CSV.

---

# 🧹 ETL Pipeline

The ETL pipeline is the core Data Engineering component.

## Extract

Raw transactions are read from:

```text
data/raw_sales.csv
```

## Transform

The pipeline performs:

### 1. Duplicate removal

Duplicate `order_id` values are identified and removed.

### 2. Missing-value handling

Missing categorical values are assigned sensible defaults.

### 3. Data validation

The pipeline validates:

- Dates
- Quantity
- Unit price
- Discount
- Categories
- Regions

### 4. Standardization

Text dimensions such as category and region are cleaned and standardized.

### 5. Feature engineering

The following analytical fields are created:

```text
gross_sales
discount_amount
revenue
estimated_cost
profit
profit_margin
order_month
order_year
order_year_month
```

### Revenue calculation

```text
Gross Sales = Quantity × Unit Price

Discount Amount = Gross Sales × Discount

Revenue = Gross Sales − Discount Amount
```

### Profit calculation

```text
Estimated Cost = Revenue × Cost Percentage

Profit = Revenue − Estimated Cost

Profit Margin = Profit / Revenue
```

---

# 🗄️ Data Storage

The cleaned dataset is stored in two formats:

### CSV

```text
data/cleaned_sales.csv
```

Useful for:

- Inspection
- Data sharing
- Lightweight analysis

### SQLite

```text
sales.db
```

Useful for:

- SQL analytics
- Structured querying
- Dashboard data access

Indexes are created on commonly queried fields such as:

```text
order_date
category
region
```

---

# 🔎 SQL Analytics

The project includes a dedicated SQL analytics file:

```text
sql/analytics.sql
```

It contains queries for:

1. Total revenue
2. Total profit
3. Total orders
4. Total customers
5. Average order value
6. Revenue by month
7. Revenue by category
8. Revenue by region
9. Profit by category
10. Top 10 products
11. Top 10 customers
12. Monthly order count
13. Average discount by category
14. Profit margin by category

This separates the **data engineering layer** from the **business analytics layer**.

---

# 🛠️ Technology Stack

| Technology | Purpose |
|---|---|
| 🐍 Python | Core programming and ETL |
| 🐼 Pandas | Data cleaning and transformation |
| 🔢 NumPy | Data generation and numerical operations |
| 🗄️ SQLite | Analytical database |
| 🔎 SQL | Business analytics |
| 📊 Plotly | Interactive visualizations |
| 🎈 Streamlit | Dashboard and web application |
| 🌐 GitHub | Version control |
| ☁️ Streamlit Community Cloud | Deployment |

---

# 📁 Project Structure

```text
ecommerce-sales-intelligence/
│
├── 📊 app.py
│
├── 📂 data/
│   ├── raw_sales.csv
│   └── cleaned_sales.csv
│
├── 📂 etl/
│   └── pipeline.py
│
├── 📂 sql/
│   └── analytics.sql
│
├── 📄 requirements.txt
├── 📄 README.md
└── 📄 .gitignore
```

The ETL pipeline also creates:

```text
sales.db
```

---

# ⚡ Quick Start

## 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/ecommerce-sales-intelligence.git
```

```bash
cd ecommerce-sales-intelligence
```

---

## 2. Create a virtual environment

### Windows

```bash
python -m venv .venv
```

```bash
.venv\Scripts\activate
```

### macOS / Linux

```bash
python3 -m venv .venv
```

```bash
source .venv/bin/activate
```

---

## 3. Install dependencies

```bash
pip install -r requirements.txt
```

---

## 4. Run the ETL pipeline

```bash
python etl/pipeline.py
```

Expected output:

```text
Number of raw records: 20100
Number of cleaned records: 20000
Number of duplicates removed: 100
Number of missing values handled: 80
Total revenue: ₹5,785,265.72
Total profit: ₹1,848,293.97
Pipeline completed successfully.
```

---

## 5. Launch the dashboard

```bash
streamlit run app.py
```

The dashboard will open in your browser.

---

# ☁️ Deploy to Streamlit Community Cloud

The application is designed to be deployed without:

- ❌ Docker
- ❌ PostgreSQL
- ❌ AWS
- ❌ Kubernetes
- ❌ Airflow
- ❌ External APIs

### Deployment steps

1. Push the project to GitHub.
2. Open Streamlit Community Cloud.
3. Sign in with GitHub.
4. Select **Create App**.
5. Choose your repository.
6. Select branch:

```text
main
```

7. Set the main file:

```text
app.py
```

8. Click **Deploy**.

The application automatically creates the data and SQLite database if they do not already exist.

---

# 🧪 Data Quality Demonstration

The project intentionally introduces a small amount of imperfect data to demonstrate real ETL practices.

For example:

```text
Raw records
    ↓
20,100
    ↓
Duplicate detection
    ↓
100 duplicates removed
    ↓
Missing-value handling
    ↓
20,000 clean records
```

This makes the project more representative of a real-world data pipeline than simply generating perfectly clean data.

---

# 💡 Business Insights

The dashboard dynamically identifies:

### 🏆 Highest Revenue Category

Which product category generates the most revenue?

### 🌎 Best Region

Which geographical region contributes the most revenue?

### 💰 Most Profitable Category

Which category contributes the most profit?

### 📦 Best-Selling Product

Which product has the highest quantity sold?

### 👑 Highest-Value Customer

Which customer generates the most revenue?

### 📅 Best-Performing Month

Which month produced the highest revenue?

All insights update automatically when dashboard filters change.

---

# 🎓 What This Project Demonstrates

This project intentionally combines **Data Engineering + Data Analytics**.

### Data Engineering

```text
Data Generation
      ↓
ETL
      ↓
Data Quality
      ↓
Transformation
      ↓
Feature Engineering
      ↓
Database Loading
```

### Data Analytics

```text
SQL
 ↓
KPIs
 ↓
Aggregations
 ↓
Trends
 ↓
Visualization
 ↓
Business Insights
```

### Final Product

```text
             DATA
              ↓
         ENGINEERING
              ↓
          ANALYTICS
              ↓
       VISUALIZATION
              ↓
     BUSINESS DECISIONS
```

---

# 📈 How I Would Scale This

This project intentionally uses a lightweight architecture because it is designed as a portfolio project.

For a production environment, I would evolve it into:

```text
Raw Data
    ↓
Cloud Object Storage
    ↓
Airflow
    ↓
Data Validation
    ↓
dbt Transformations
    ↓
PostgreSQL / Data Warehouse
    ↓
BI / Streamlit
```

### Possible improvements

- PostgreSQL instead of SQLite
- Cloud storage
- Airflow orchestration
- dbt transformations
- Incremental pipelines
- Data quality monitoring
- CI/CD
- Docker
- Real-time event ingestion
- ML-based sales forecasting
- Automated alerts

---

# 🔮 Future Roadmap

### Phase 1 — Current

- [x] Synthetic data generation
- [x] ETL pipeline
- [x] Data cleaning
- [x] Feature engineering
- [x] SQLite database
- [x] SQL analytics
- [x] Streamlit dashboard
- [x] Product analytics
- [x] Customer analytics
- [x] Business insights

### Phase 2 — Production Architecture

- [ ] PostgreSQL
- [ ] Airflow
- [ ] dbt
- [ ] Cloud storage
- [ ] CI/CD

### Phase 3 — Advanced Analytics

- [ ] Sales forecasting
- [ ] Customer churn prediction
- [ ] Customer lifetime value
- [ ] Product recommendation
- [ ] Real-time analytics

---

# 🧑‍💻 summary




> **"I built an end-to-end E-Commerce Sales Intelligence Platform using Python, Pandas, NumPy, SQLite, SQL, Streamlit and Plotly. I generated more than 20,000 realistic transactions and created an ETL pipeline that extracts the raw CSV, removes duplicates, handles missing values, validates data and performs feature engineering. I calculated metrics such as revenue, discount amount, estimated cost, profit and profit margin. The cleaned data is loaded into SQLite, where I use SQL to perform business analytics such as monthly revenue, category performance, regional performance and top customers and products. Finally, I built an interactive Streamlit dashboard with KPI cards, product analytics, customer segmentation, filters and dynamic business insights. The application is GitHub-ready and deployable through Streamlit Community Cloud."**

---

# 📄 Key points 

**E-Commerce Sales Intelligence Platform | Python, Pandas, NumPy, SQL, SQLite, Streamlit, Plotly**

- Developed an end-to-end **Data Engineering and Analytics pipeline** processing **20K+ e-commerce transactions** using Python, Pandas and NumPy.
- Implemented ETL workflows including **deduplication, missing-value handling, validation, standardization and feature engineering**.
- Engineered revenue, discount, cost, profit, profit-margin and time-based analytical features.
- Built SQL analytics for **revenue, profit, AOV, customer, product, category, regional and monthly performance**.
- Developed an interactive **Streamlit + Plotly dashboard** featuring KPI monitoring, product analytics, customer segmentation, dynamic filtering and CSV export.
- Prepared the application for **GitHub version control and Streamlit Community Cloud deployment**.

---

# 🌐 GitHub Repository

If you found this project useful, feel free to explore the code and architecture.

```text
⭐ Star the repository
🍴 Fork the project
💡 Build your own version
```

---

# 👨‍💻 Author

**Nitin Kumar Rajvanshi**

Data Analytics | Data Engineering | Python | SQL

📌 Built as a portfolio project demonstrating an end-to-end analytics workflow.

---

# ⭐ Final Takeaway

> **Good analytics does not start with a dashboard.**
>
> It starts with reliable data.

This project demonstrates the complete journey:

```text
RAW DATA
   ↓
CLEAN DATA
   ↓
ENGINEERED DATA
   ↓
DATABASE
   ↓
SQL
   ↓
ANALYTICS
   ↓
DASHBOARD
   ↓
BUSINESS INSIGHTS
   ↓
BETTER DECISIONS
```

**Built with Python. Powered by SQL. Visualized with Streamlit. Designed for business decisions.**
