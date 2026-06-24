# Star Schema

## Overview
The Gold layer of this project is modeled using a **Star Schema** to support business intelligence reporting and dashboard analytics. A star schema is a dimensional modeling approach where a central **fact table** is connected to multiple surrounding **dimension tables**.

This structure is commonly used in data warehouses because it:
- simplifies analytical queries
- improves dashboard performance
- makes business metrics easier to understand
- separates measurable events from descriptive business attributes

---

## Star Schema in This Project
The e-commerce BI pipeline organizes Gold layer data into a dimensional model for reporting. The central transactional dataset is represented by a **fact table**, while descriptive attributes such as customer, product, and date are stored in **dimension tables**.

### Core Gold tables
**Fact table**
- `gld_fact_order_items`

**Dimension tables**
- `gld_dim_products`
- `gld_dim_customers`
- `gld_dim_date`

In some cases, a denormalized analytical view such as `fact_transactions_denorm` can also be created for dashboard consumption, but the star schema itself is centered around the fact table and dimensions.

---

## Fact Table

### `gld_fact_order_items`
The fact table stores the measurable transactional events of the business. Each row typically represents an order item or transaction-level event.

### Typical fact attributes
Depending on the implementation, the fact table may include:
- order identifiers
- product key
- customer key
- date key
- quantity sold
- unit price
- gross revenue / net revenue
- discount amount
- tax amount
- coupon usage indicators
- channel or transaction attributes

### Role of the fact table
The fact table is responsible for storing the numerical measures used in analysis, such as:
- total sales
- total quantity sold
- total discounts
- total tax
- order counts
- revenue trends

It acts as the central table for analytical aggregations.

---

## Dimension Tables

### 1. `gld_dim_products`
The product dimension stores descriptive information about products.

Typical attributes may include:
- product identifier
- product name / label
- brand
- category
- material
- color
- product type or classification

This table is used for product-level analysis such as:
- top-selling products
- revenue by category
- brand performance
- product mix analysis

---

### 2. `gld_dim_customers`
The customer dimension stores customer-related descriptive attributes.

Typical attributes may include:
- customer identifier
- customer name / code
- country
- region
- state
- city
- customer segment or classification

This table supports:
- customer insights
- regional performance analysis
- customer count and spend analysis
- country-wise revenue reporting

---

### 3. `gld_dim_date`
The date dimension standardizes time-based reporting.

Typical attributes may include:
- date key
- transaction date
- day
- month
- month name
- quarter
- year
- day of week

This dimension supports:
- monthly sales trends
- daily revenue trends
- weekday vs weekend analysis
- period-based financial reporting

---

## Relationships in the Star Schema
The fact table joins to the dimensions through keys.

Typical relationships:
- `gld_fact_order_items.product_sk` → `gld_dim_products.product_sk`
- `gld_fact_order_items.customer_sk` → `gld_dim_customers.customer_sk`
- `gld_fact_order_items.date_sk` → `gld_dim_date.date_sk`

These relationships allow business users to aggregate fact metrics by product, customer, or time attributes without storing repeated descriptive data in the fact table itself.

---

## Why Star Schema Was Used
A star schema is appropriate for this project because the goal is not just storage, but **analytics and reporting**. It provides:

### 1. Faster reporting
Fact tables can be aggregated quickly by joining a small number of dimensions.

### 2. Simpler BI queries
Dashboard queries become more readable and easier to maintain.

### 3. Better business interpretation
Measures such as sales and discounts can be analyzed across dimensions like product, region, and date.

### 4. Scalable design
Additional dimensions or measures can be added later without redesigning the entire pipeline.

---

## Example Analytical Use Cases
The star schema enables queries such as:
- total revenue by month
- top categories by sales
- customer revenue by country
- average order value by channel
- discount amount by product category
- monthly tax and net revenue trends

These use cases directly power the dashboards built on top of the Gold layer.

---

## Star Schema vs Denormalized View
This project may also expose a reporting-friendly denormalized table or view such as `fact_transactions_denorm` for easier dashboarding. However, the star schema remains the core warehouse design because it:
- keeps the data model organized
- avoids excessive duplication of descriptive fields
- supports flexible BI reporting
- aligns with standard data warehouse practices

---

## Summary
The star schema in this project transforms cleaned e-commerce data into a structured analytical model centered around `gld_fact_order_items` and supported by product, customer, and date dimensions. This design is a key part of the Gold layer and enables efficient, scalable, and business-friendly reporting across the entire dashboard suite.
