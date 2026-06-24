# Dashboard Summary

## Overview
The final Gold layer of this project powers a suite of **E-Commerce BI Dashboards** built to analyze sales performance, customer behavior, product trends, and financial metrics. These dashboards are designed to present business-ready insights from the transformed Databricks pipeline in a clear and decision-oriented format.

The dashboard layer consumes Gold analytical tables and views, especially the fact and dimension outputs created during the Medallion pipeline.

---

## Dashboard Suite
The project includes multiple dashboards, each focused on a specific business area:

1. **Executive BI Dashboard**
2. **Sales Analytics Dashboard**
3. **Customer Insights Dashboard**
4. **Product Analytics Dashboard**
5. **Financial Analytics Dashboard**

Together, these dashboards provide a complete analytical view of the e-commerce business.

---

# 1. Executive BI Dashboard

## Purpose
The Executive BI Dashboard provides a high-level business overview for leadership and decision-makers. It focuses on core KPIs and overall performance trends.

## Typical metrics shown
- total revenue
- total orders
- total customers
- average order value
- total items sold
- coupon usage rate

## Typical visuals
- KPI cards for business summary
- revenue trend over time
- sales by channel
- top categories by revenue
- top brands by revenue
- quick performance comparison views

## Business value
This dashboard helps stakeholders quickly understand overall business performance and identify major trends without going into detailed operational analysis.

---

# 2. Sales Analytics Dashboard

## Purpose
The Sales Analytics Dashboard focuses on transaction-level sales performance and revenue behavior across time, channels, brands, and categories.

## Typical metrics shown
- total sales
- total orders
- average order value
- total quantity sold

## Typical visuals
- daily revenue trend
- monthly revenue trend
- sales by category
- top brands by revenue
- revenue by channel over time
- weekday / day-of-week sales comparison

## Business value
This dashboard helps identify:
- sales growth patterns
- peak revenue periods
- top-performing categories and brands
- channel-level sales contribution

---

# 3. Customer Insights Dashboard

## Purpose
The Customer Insights Dashboard is built to analyze customer distribution, geography, customer value, and purchase behavior.

## Typical metrics shown
- total customers
- total revenue
- average customer value
- average orders per customer
- repeat customer rate or purchase frequency metrics

## Typical visuals
- revenue distribution by country
- top countries by revenue
- customer purchase frequency histogram
- revenue by region
- customer count by region
- customer metrics by country table

## Business value
This dashboard helps answer:
- where the highest-value customers are located
- which countries or regions contribute most to revenue
- how frequently customers purchase
- how customer concentration differs geographically

---

# 4. Product Analytics Dashboard

## Purpose
The Product Analytics Dashboard evaluates product-level and category-level business performance.

## Typical metrics shown
- total products
- total revenue
- total units sold
- average unit price

## Typical visuals
- revenue by category
- top brands by revenue
- product revenue over time
- category distribution
- top products by revenue
- product contribution by category / brand

## Business value
This dashboard helps identify:
- best-selling products
- strongest product categories
- top-performing brands
- product mix contribution to overall sales

---

# 5. Financial Analytics Dashboard

## Purpose
The Financial Analytics Dashboard focuses on revenue composition, discounts, taxes, and financial quality of sales.

## Typical metrics shown
- gross revenue
- net revenue
- total discounts
- total tax
- total transactions
- discount-related KPIs

## Typical visuals
- transaction volume trend
- discount trend over time
- revenue breakdown table
- average transaction value by channel
- coupon vs non-coupon revenue comparison
- channel revenue mix
- top products by net revenue

## Business value
This dashboard helps analyze:
- impact of discounts on revenue
- tax and gross-to-net relationships
- channel-level financial contribution
- product-level profitability and net revenue behavior

---

## Common Dashboard Data Sources
The dashboards are built from the Gold layer, primarily using:
- `gld_fact_order_items`
- `gld_dim_products`
- `gld_dim_customers`
- `gld_dim_date`
- `fact_transactions_denorm`

These datasets provide the measures and attributes needed for KPI cards, trend charts, category comparisons, customer geography, and financial reporting.

---

## Dashboard Design Goals
The dashboard layer in this project was created with the following objectives:
- present business KPIs clearly
- support exploratory analysis across multiple business functions
- highlight trends over time
- enable category, customer, and channel comparisons
- showcase the analytical value of the Gold data model

---

## Business Impact of the Dashboard Layer
The dashboard suite demonstrates how a properly designed data engineering pipeline can be transformed into business-facing insights. It shows the full value chain of the project:

**raw e-commerce data → cleaned ETL pipeline → Gold warehouse model → executive and analytical dashboards**

This makes the project useful not only as a data engineering portfolio project, but also as a BI and analytics showcase.

---

## Summary
The dashboard layer is the final consumption stage of the E-Commerce BI Pipeline. It translates the outputs of the Medallion Architecture and Gold data model into interactive, business-friendly analytics views covering executive performance, sales, customers, products, and financials. Together, these dashboards complete the project as a full end-to-end business intelligence solution.
