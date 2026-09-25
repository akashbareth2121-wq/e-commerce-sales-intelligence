-- E-Commerce Sales Intelligence Platform
-- Run against sales.db after executing etl/pipeline.py.

-- 1. Total revenue
SELECT ROUND(SUM(revenue), 2) AS total_revenue
FROM sales;

-- 2. Total profit
SELECT ROUND(SUM(profit), 2) AS total_profit
FROM sales;

-- 3. Total orders
SELECT COUNT(DISTINCT order_id) AS total_orders
FROM sales;

-- 4. Total customers
SELECT COUNT(DISTINCT customer_id) AS total_customers
FROM sales;

-- 5. Average order value
SELECT ROUND(SUM(revenue) / COUNT(DISTINCT order_id), 2) AS average_order_value
FROM sales;

-- 6. Revenue by month
SELECT order_year_month,
       ROUND(SUM(revenue), 2) AS revenue
FROM sales
GROUP BY order_year_month
ORDER BY order_year_month;

-- 7. Revenue by category
SELECT category,
       ROUND(SUM(revenue), 2) AS revenue
FROM sales
GROUP BY category
ORDER BY revenue DESC;

-- 8. Revenue by region
SELECT region,
       ROUND(SUM(revenue), 2) AS revenue
FROM sales
GROUP BY region
ORDER BY revenue DESC;

-- 9. Profit by category
SELECT category,
       ROUND(SUM(profit), 2) AS profit
FROM sales
GROUP BY category
ORDER BY profit DESC;

-- 10. Top 10 products by revenue
SELECT product,
       ROUND(SUM(revenue), 2) AS revenue
FROM sales
GROUP BY product
ORDER BY revenue DESC
LIMIT 10;

-- 11. Top 10 customers by revenue
SELECT customer_id,
       customer_name,
       ROUND(SUM(revenue), 2) AS revenue
FROM sales
GROUP BY customer_id, customer_name
ORDER BY revenue DESC
LIMIT 10;

-- 12. Monthly order count
SELECT order_year_month,
       COUNT(DISTINCT order_id) AS orders
FROM sales
GROUP BY order_year_month
ORDER BY order_year_month;

-- 13. Average discount by category
SELECT category,
       ROUND(AVG(discount) * 100, 2) AS average_discount_percent
FROM sales
GROUP BY category
ORDER BY average_discount_percent DESC;

-- 14. Profit margin by category
SELECT category,
       ROUND(SUM(profit) / NULLIF(SUM(revenue), 0) * 100, 2) AS profit_margin_percent
FROM sales
GROUP BY category
ORDER BY profit_margin_percent DESC;
