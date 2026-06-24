# Project Workflow

## Overview
This project implements an end-to-end **E-Commerce Business Intelligence Pipeline** on **Databricks** using a **Medallion Architecture** design. The workflow ingests raw e-commerce CSV data, transforms it through Bronze, Silver, and Gold layers, and produces business-ready analytical datasets that power dashboards for executive and operational reporting.

The pipeline is designed to simulate a real-world data engineering workflow with:
- Layered ETL processing
- Delta Lake based storage
- Star schema modeling
- PySpark transformations
- Databricks notebook orchestration
- BI dashboard consumption

---

## End-to-End Workflow

### 1. Raw Data Ingestion
The workflow starts by loading raw CSV datasets into the Databricks environment. These files contain source information related to:
- products
- brands
- categories
- customers
- calendar/date
- order items / transactions

These files are stored in the source layer and ingested into the **Bronze layer** without major transformation.

**Objective:** preserve raw data exactly as received while establishing a structured landing zone for downstream processing.

---

### 2. Bronze Layer Processing
The Bronze layer stores the ingested raw data as Delta tables. At this stage:
- schemas are defined
- ingestion metadata can be captured
- raw records are persisted in their original form
- source files are standardized into a queryable table format

Typical Bronze outputs include:
- `brz_brands`
- `brz_category`
- `brz_products`
- `brz_customers`
- `brz_date`
- `brz_order_items`

**Objective:** create a reliable raw-data foundation for further transformations.

---

### 3. Silver Layer Processing
The Silver layer is responsible for data cleaning and transformation. This is where the project applies core ETL logic such as:
- null handling
- deduplication
- datatype corrections
- standardization of categorical values
- quality checks
- enrichment and normalization

For dimension entities, Silver tables act as the cleansed version of the Bronze data.

Typical Silver outputs include:
- `slv_brands`
- `slv_category`
- `slv_products`
- `slv_customers`
- `slv_calendar`
- `slv_order_items`

**Objective:** produce trusted, cleaned, and transformation-ready datasets.

---

### 4. Gold Layer Processing
The Gold layer contains business-ready analytical tables. In this project, the Gold layer is used to build:
- dimension tables
- fact tables
- denormalized analytical views
- KPI-ready datasets for dashboards

This layer is modeled using a **star schema** so that reporting and dashboard queries can run efficiently.

Typical Gold outputs include:
- `gld_dim_products`
- `gld_dim_customers`
- `gld_dim_date`
- `gld_fact_order_items`
- `fact_transactions_denorm` (analytical reporting view)

**Objective:** create optimized reporting datasets for business intelligence and analytics.

---

## Notebook Execution Flow

The Databricks workflow follows a staged notebook execution pattern.

### Setup
1. **Setup notebook**
   - Creates catalog / schema / database objects
   - Defines storage locations
   - Prepares environment for pipeline execution

### Dimension pipeline
2. **Dimension Bronze notebook**
   - Loads raw dimension datasets into Bronze tables

3. **Dimension Silver notebook**
   - Cleans and standardizes dimension data

4. **Dimension Gold notebook**
   - Builds dimension tables with analytical structure and surrogate keys where required

### Fact pipeline
5. **Fact Bronze notebook**
   - Loads order / transaction level data into Bronze

6. **Fact Silver notebook**
   - Cleans and validates order item level transactional data

7. **Fact Gold notebook**
   - Builds fact tables and denormalized analytical views for reporting

---

## Orchestration Logic
The project is structured so the workflow can be orchestrated in a sequential order using **Databricks Jobs / Workflows**.

Recommended dependency order:
1. Setup notebook
2. Dimension Bronze
3. Dimension Silver
4. Dimension Gold
5. Fact Bronze
6. Fact Silver
7. Fact Gold
8. Dashboard / BI layer refresh

This sequencing ensures that:
- source structures exist before ingestion begins
- dimensions are prepared before fact modeling
- reporting views are refreshed only after Gold data is available

---

## Dashboard Consumption
Once the Gold layer is prepared, business dashboards can be built on top of the final reporting tables. In this project, dashboards are designed for:
- Executive BI overview
- Sales analytics
- Customer insights
- Product analytics
- Financial analytics

These dashboards consume Gold layer outputs and provide business users with a clear view of revenue, orders, customer behavior, product performance, and financial metrics.

---

## Key Engineering Outcomes
This workflow demonstrates:
- practical implementation of Medallion Architecture
- ETL pipeline design using PySpark
- layered Delta Lake transformations
- data warehousing using star schema principles
- dashboard-oriented analytical modeling
- orchestration of notebook-based data pipelines in Databricks

---

## Summary
The workflow of this project reflects a realistic modern data engineering pipeline: raw data is ingested into Bronze, transformed into clean Silver tables, modeled into Gold business tables, and then consumed through interactive dashboards. This structure makes the project suitable for showcasing data engineering, data modeling, and BI reporting capabilities in a single end-to-end implementation.
