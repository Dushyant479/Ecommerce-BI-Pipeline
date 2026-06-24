# Databricks notebook source
import pyspark.sql.functions as F
from pyspark.sql.types import *
from pyspark.sql import *

# COMMAND ----------

catalog_name = "ecommerce"

# COMMAND ----------

# MAGIC %md
# MAGIC #Products

# COMMAND ----------

df_products = spark.table(f"{catalog_name}.silver.slv_products")
df_brands = spark.table(f"{catalog_name}.silver.slv_brands")
df_category = spark.table(f"{catalog_name}.silver.slv_category")

# COMMAND ----------

df_products.createOrReplaceTempView("v_products")
df_brands.createOrReplaceTempView("v_brands")
df_category.createOrReplaceTempView("v_category")

# COMMAND ----------

display(spark.sql("select * from v_products limit 5"))

# COMMAND ----------

spark.sql(f"USE CATALOG {catalog_name}")

# COMMAND ----------

# DBTITLE 1,Cell 7
# MAGIC %sql
# MAGIC WITH brands_category AS(
# MAGIC     SELECT
# MAGIC     b.brand_name,
# MAGIC     b.brand_code,
# MAGIC     c.category_name,
# MAGIC     c.category_code
# MAGIC     FROM v_brands b
# MAGIC     INNER JOIN v_category c
# MAGIC     ON b.category_code = c.category_code
# MAGIC )
# MAGIC SELECT
# MAGIC p.product_id,
# MAGIC p.sku,
# MAGIC p.category_code,
# MAGIC COALESCE(bc.category_name, 'Not Available') AS category_name,
# MAGIC p.brand_code,
# MAGIC COALESCE(bc.brand_name, 'Not Available') AS brand_name,
# MAGIC p.color,
# MAGIC p.size,
# MAGIC p.material,
# MAGIC p.weight_grams,
# MAGIC p.length_cm,
# MAGIC p.width_cm,
# MAGIC p.height_cm,
# MAGIC p.rating_count,
# MAGIC p.file_name,
# MAGIC p.ingest_timestamp
# MAGIC FROM v_products p
# MAGIC LEFT JOIN brands_category bc
# MAGIC ON p.brand_code = bc.brand_code;

# COMMAND ----------

# MAGIC %md
# MAGIC #Customers

# COMMAND ----------

india_region = {
    "MH":"West","GJ":"West","RJ":"West",
    "KA":"South","TN":"South","TS":"South","AP":"South","KL":"South",
    "UP":"North","WB":"North","DL":"North"
}
australia_region = {"VIC":"SouthEast","WA":"West","NSW":"East","QLD":"NorthEast"}
uk_region={
    "ENG":"England","WLS":"Wales","NIR":"Northern Ireland","SCT":"Scotland"
}
us_region={
    "MA":"NorthEast","FL":"South","NJ":"NorthEast","CA":"West",
    "NY":"NorthEast","TX":"South"
}
uae_region = {
    "AUH":"Abu Dhabi","DU":"Dubai","SHJ":"Sharjah"
}

singapore_region = {
    "SG":"Singapore"
}

canada_region = {
    "BC":"West","AB":"West","ON":"East","QC":"East","NS":"East","IL":"Other"
}

country_state_map ={
    "India":india_region,
    "Australia":australia_region,
    "UK":uk_region,
    "US":us_region,
    "UAE":uae_region,
    "Singapore":singapore_region,
    "Canada":canada_region
}

# COMMAND ----------

country_state_map

# COMMAND ----------

rows=[]
for country,states in country_state_map.items():
    for state_code,region in states.items():
        rows.append(Row(country=country,state=state_code,region=region))
rows[:10]

# COMMAND ----------

df_region_mapping = spark.createDataFrame(rows)

df_region_mapping.show(truncate=False)

# COMMAND ----------

df_silver = spark.table(f"{catalog_name}.silver.slv_customers")
display(df_silver)


# COMMAND ----------

df_gold = df_silver.join(df_region_mapping,on=['country','state'],how='left')
df_gold = df_gold.fillna({'region':'Other'})
display(df_gold.limit(5))

# COMMAND ----------

df_gold.write.format("delta").mode("overwrite").option("mergeSchema","true").saveAsTable(f"{catalog_name}.gold.gld_dim_customers")

# COMMAND ----------

# MAGIC %md
# MAGIC #Date/Calendar

# COMMAND ----------

df_sil_cal = spark.table(f"{catalog_name}.silver.slv_calendar")
display(df_sil_cal.limit(5))


# COMMAND ----------

df_gold_cal = df_sil_cal.withColumn("date_id",F.date_format(F.col("date"),"yyyyMMdd").cast('int'))
df_gold_cal = df_gold_cal.withColumn("month_name",F.date_format(F.col("date"),"MMMM"))
df_gold_cal = df_gold_cal.withColumn("is_weekend",F.when(F.col("day_name").isin(["Saturday","Sunday"]),1).otherwise(0))
display(df_gold_cal.limit(5))

# COMMAND ----------

# DBTITLE 1,Cell 20
desired_columns_order = ['date_id','date','year','month_name','day_name','is_weekend','quarter','week','_ingested_at','_source_file']
df_gold_cal = df_gold_cal.select(desired_columns_order)
display(df_gold_cal.limit(5))

# COMMAND ----------

df_gold_cal.write.format("delta").mode("overwrite").option("mergeSchema","true").saveAsTable(f"{catalog_name}.gold.gld_dim_date")

# COMMAND ----------

