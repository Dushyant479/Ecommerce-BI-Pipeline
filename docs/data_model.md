# Data Model

## Overview
The data model of this project is designed to support an end-to-end **E-Commerce Business Intelligence Pipeline** on Databricks. It combines Medallion Architecture principles with dimensional modeling so that raw operational data can be transformed into analytical datasets suitable for reporting and dashboarding.

At a high level, the model progresses through three stages:
1. **Raw operational source data**
2. **Layered Medallion transformations**
3. **Gold analytical model for reporting**

---

## Source Entities
The project uses multiple source datasets that represent key e-commerce business entities.

### Main source datasets
- **Brands** – brand-level reference data
- **Category** – product category classification data
- **Products** – product attributes and product master information
- **Customers** – customer-level information such as region/country
- **Date / Calendar** – time and reporting attributes
- **Order Items / Transactions** – transactional order-level sales data

These entities collectively support both master-data modeling and transactional sales analytics.

---

## Layered Data Model

## 1. Bronze Data Model
The Bronze layer contains raw ingested tables. These are close to the source format and mainly serve as a landing layer.

### Bronze tables
- `brz_brands`
- `brz_category`
- `brz_products`
- `brz_customers`
- `brz_date`
- `brz_order_items`

### Role of Bronze
- preserve source-level structure
- store raw data for traceability
- enable repeatable transformation pipelines
- isolate ingestion from business logic

---

## 2. Silver Data Model
The Silver layer contains cleaned and standardized versions of the source entities.

### Silver tables
- `slv_brands`
- `slv_category`
- `slv_products`
- `slv_customers`
- `slv_calendar`
- `slv_order_items`

### Role of Silver
- clean inconsistent source values
- standardize datatypes and formats
- remove duplicates and invalid records
- prepare datasets for dimensional modeling

Silver tables are not yet final reporting tables, but they are trusted transformation outputs used to build Gold.

---

## 3. Gold Data Model
The Gold layer contains business-ready tables designed for analytics.

### Gold dimension tables
- `gld_dim_products`
- `gld_dim_customers`
- `gld_dim_date`

### Gold fact table
- `gld_fact_order_items`

### Gold analytical view
- `fact_transactions_denorm`

---

## Dimension Modeling

### Product Dimension
The product dimension consolidates descriptive product attributes into a single business entity. It may include:
- product ID
- category
- brand
- material
- color
- product-related classifications

**Business use:** product revenue analysis, category trends, brand performance, product mix analysis.

---

### Customer Dimension
The customer dimension stores customer-level descriptive information such as:
- customer ID
- country
- state
- region
- customer-related segmentation attributes

**Business use:** customer analytics, regional sales, top customer reporting, geography-based dashboards.

---

### Date Dimension
The date dimension standardizes time-based reporting attributes:
- date key
- date
- month
- month name
- year
- quarter
- day of week

**Business use:** monthly trends, daily sales analysis, weekday patterns, financial period reporting.

---

## Fact Modeling

### Order Item Fact
The fact table stores transaction-level measures and keys linking to dimensions.

Typical measures may include:
- quantity
- unit price
- gross revenue
- net revenue
- discount amount
- tax amount
- order count indicators
- coupon usage flags

Typical foreign keys may include:
- `product_sk`
- `customer_sk`
- `date_sk`

**Business use:** this table is the primary source for sales, customer, product, and financial dashboard metrics.

---

## Denormalized Reporting Model
To simplify dashboard consumption, the project may expose a denormalized Gold analytical view such as `fact_transactions_denorm`. This view combines fact measures with descriptive dimension attributes into a reporting-friendly structure.

### Why a denormalized view helps
- reduces dashboard query complexity
- simplifies BI layer development
- makes metric creation easier for reporting tools
- improves usability for self-service analytics

This is especially useful for dashboarding where product, customer, time, and transaction metrics are frequently analyzed together.

---

## Logical Relationship Flow
The data model can be understood in the following way:

### Source to Bronze
Raw CSV source files are loaded into raw Bronze tables.

### Bronze to Silver
Bronze tables are cleaned and transformed into standardized Silver tables.

### Silver to Gold
Silver data is used to create:
- product dimension
- customer dimension
- date dimension
- order item fact table
- denormalized analytical reporting view

### Gold to Dashboard
The final Gold outputs are consumed by Databricks dashboards for business analysis.

---

## Business Areas Covered by the Data Model
The Gold data model supports multiple business reporting areas:

### Sales analytics
- revenue trends
- order volume
- category performance
- brand performance
- channel performance

### Customer analytics
- customer count
- revenue by country / region
- customer purchase frequency
- average spend per customer

### Product analytics
- top products
- product category distribution
- unit sales
- brand contribution

### Financial analytics
- gross revenue
- net revenue
- discounts
- taxes
- coupon impact

---

## Design Strengths of the Model
This data model is effective because it:
- separates ingestion, transformation, and reporting layers
- supports scalable ETL development
- enables star-schema based analytics
- balances normalized warehouse design with denormalized reporting needs
- aligns with enterprise data engineering practices

---

## Summary
The project’s data model combines raw e-commerce source entities, Medallion Architecture processing, and Gold-layer dimensional modeling into a complete BI-ready analytical system. It is structured to support dashboard development, KPI reporting, and scalable data engineering workflows in Databricks.
