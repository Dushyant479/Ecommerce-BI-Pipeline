# Medallion Architecture

## Overview
This project follows the **Medallion Architecture** pattern in Databricks to organize data into progressive quality layers. The Medallion model improves reliability, traceability, and maintainability by separating raw ingestion, cleaned transformations, and business-ready analytical outputs.

The three core layers used in this project are:

- **Bronze** – raw ingested data
- **Silver** – cleaned and standardized data
- **Gold** – business-ready analytical data

---

## Why Medallion Architecture?
Using Medallion Architecture in this project provides several advantages:
- clear separation of raw, cleansed, and analytical data
- easier debugging and data lineage tracking
- better support for incremental development
- reusable transformation logic
- simplified dashboard consumption from Gold tables

Instead of transforming raw files directly into reports, the project moves data through well-defined layers so each stage has a specific responsibility.

---

## Bronze Layer

### Purpose
The Bronze layer acts as the **raw ingestion layer**. It stores data as close to the source format as possible.

### What happens in Bronze?
- raw CSV files are loaded into Delta tables
- original source structure is preserved
- basic schema handling is applied
- minimal validation may be performed
- ingestion-ready raw tables are created

### Example Bronze tables
- `brz_brands`
- `brz_category`
- `brz_products`
- `brz_customers`
- `brz_date`
- `brz_order_items`

### Benefits of Bronze
- preserves source data for reprocessing
- provides a stable landing layer
- separates ingestion from transformation logic
- supports data lineage and auditing

---

## Silver Layer

### Purpose
The Silver layer is the **cleansed and standardized transformation layer**. Data from Bronze is refined here before it is used for analytics.

### What happens in Silver?
- null values are handled
- duplicates are removed
- invalid or inconsistent values are standardized
- datatypes are corrected
- business-friendly columns are prepared
- source inconsistencies are resolved

### Example Silver tables
- `slv_brands`
- `slv_category`
- `slv_products`
- `slv_customers`
- `slv_calendar`
- `slv_order_items`

### Benefits of Silver
- improves data quality before analytical modeling
- creates reusable cleaned datasets
- centralizes business transformation logic
- prepares data for star schema and reporting

---

## Gold Layer

### Purpose
The Gold layer is the **business-ready analytical layer**. It contains the final curated datasets used by dashboards and reporting solutions.

### What happens in Gold?
- dimension tables are created
- fact tables are modeled
- surrogate keys can be generated where needed
- denormalized analytical views are prepared
- KPI-ready datasets are exposed for BI dashboards

### Example Gold outputs
- `gld_dim_products`
- `gld_dim_customers`
- `gld_dim_date`
- `gld_fact_order_items`
- `fact_transactions_denorm`

### Benefits of Gold
- optimized for analytical queries
- easier dashboard development
- supports star schema reporting
- exposes business metrics in a usable format

---

## Flow of Data in This Project
The data flow in this project follows the sequence below:

1. Raw CSV files are loaded into Bronze tables  
2. Bronze tables are transformed and cleaned into Silver tables  
3. Silver tables are modeled into Gold dimensions and facts  
4. Gold outputs are used to create dashboards and business reports  

This layered progression ensures that raw ingestion, data quality improvement, and analytical modeling are handled independently and systematically.

---

## Role of Databricks and Delta Lake
The Medallion design is implemented in **Databricks** with **PySpark** and **Delta Lake**.

### Databricks is used for:
- notebook-based ETL development
- scalable distributed data processing
- workflow orchestration
- SQL and dashboard integration

### Delta Lake is used for:
- table storage and management
- reliable transactional writes
- schema enforcement / compatibility support
- improved performance for analytics workloads

---

## Practical Value in This Project
In the context of this e-commerce BI pipeline, the Medallion Architecture helps organize the entire solution into a clean engineering workflow:

- Bronze stores source e-commerce data
- Silver improves data quality and consistency
- Gold supports business reporting such as revenue, orders, customers, products, and finance dashboards

This structure mirrors how enterprise data engineering teams build production-ready analytics pipelines.

---

## Summary
The Medallion Architecture is the backbone of this project. It enables the pipeline to move from raw operational data to clean, business-ready insights in a structured and scalable way. By separating Bronze, Silver, and Gold responsibilities, the project demonstrates strong data engineering design principles and creates a solid foundation for downstream BI dashboards.
