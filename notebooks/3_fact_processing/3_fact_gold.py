# Databricks notebook source
from pyspark.sql.types import *
import pyspark.sql.functions as F
from pyspark.sql.functions import *
catalog_name = "ecommerce"

# COMMAND ----------

df = spark.table(f"{catalog_name}.silver.slv_order_items")
df.limit(10).display()

# COMMAND ----------

#1) Add gross amount
df = df.withColumn(
    "gross_amount",
    F.col("quantity") * F.col("unit_price")
)
 
#2) Add discount_amount (discount_pct is already numeric, eg. 21 -> 21%)
df = df.withColumn(
    "discount_amount",
    F.ceil(F.col("gross_amount") * (F.col("discount_pct")/100.0))
)

df=df.withColumn(
    "sales_amount",
    F.col("gross_amount") - F.col("discount_amount") + F.col("tax_amount")
)

df=df.withColumn("date_id",F.date_format(F.col("dt"),"yyyyMMdd").cast(IntegerType()))

df=df.withColumn(
    "coupon_flag",
    F.when(F.col("coupon_code").isNotNull(),F.lit(1)).otherwise(F.lit(0))
)
df.limit(5).display()

# COMMAND ----------

fx_rates={
    "INR":1.00,
    "AED":24.18,
    "AUD":57.55,
    "CAD":62.93,
    "GBP":117.98,
    "SGD":68.18,
    "USD":88.29
}
rates = [(k,float(v)) for k,v in fx_rates.items()]
rates_df= spark.createDataFrame(rates,["currency","inr_rate"])
rates_df.show()

# COMMAND ----------

df = (
    df
    .join(
        rates_df,
        rates_df.currency==F.upper(F.trim(F.col("unit_price_currency"))),
        "left"
    )
    .withColumn("sales_amount_inr",F.col("sales_amount") * F.col("inr_rate"))
    .withColumn("sales_amount_inr",F.ceil(F.col("sales_amount_inr")))
)

# COMMAND ----------

df.limit(5).display()

# COMMAND ----------

orders_gold_df = df.select(
    F.col("date_id"),
    F.col("dt").alias("transaction_date"),
    F.col("order_ts").alias("transaction_ts"),
    F.col("order_id").alias("transaction_id"),
    F.col("customer_id"),
    F.col("item_seq").alias("seq_no"),
    F.col("product_id"),
    F.col("channel"),
    F.col("coupon_code"),
    F.col("coupon_flag"),
    F.col("unit_price_currency"),
    F.col("quantity"),
    F.col("unit_price"),
    F.col("gross_amount"),
    F.col("discount_pct").alias("discount_percent"),
    F.col("discount_amount"),
    F.col("tax_amount"),
    F.col("sales_amount").alias("net_amount"),
    F.col("sales_amount_inr").alias("net_amount_inr")
)

# COMMAND ----------

orders_gold_df.write.format("delta").mode("overwrite").option("mergeSchema","true").saveAsTable(f"{catalog_name}.gold.gld_fact_order_items")

# COMMAND ----------

# MAGIC %sql
# MAGIC CREATE OR REPLACE VIEW ecommerce.gold.fact_transactions_denorm as (
# MAGIC SELECT i.*,c.year,c.month_name,c.day_name,c.is_weekend,c.quarter,c.week,p.sku,p.category_code,p.category_name,p.brand_code,p.brand_name,p.color,p.size,p.rating_count,extract(HOUR FROM transaction_ts) as hour_of_day
# MAGIC FROM ecommerce.gold.gld_fact_order_items i JOIN 
# MAGIC ecommerce.gold.gld_dim_date c on i.date_id = c.date_id join 
# MAGIC ecommerce.gold.gld_dim_products p on i.product_id = p.product_id);

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT * FROM ecommerce.gold.fact_transactions_denorm