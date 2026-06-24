# Databricks notebook source
from pyspark.sql.types import *
import pyspark.sql.functions as F
from pyspark.sql.functions import *
catalog_name = "ecommerce"

# COMMAND ----------

df = spark.table('ecommerce.bronze.brz_order_items')
df.display()

# COMMAND ----------

df = df.dropDuplicates(['order_id','item_seq'])
df = df.withColumn('quantity',when(col('quantity')=="Two",2).otherwise(col('quantity')).cast('int'))

df = df.withColumn('unit_price',regexp_replace('unit_price',"[$]","").cast("double"))

df = df.withColumn('discount_pct',regexp_replace('discount_pct','%',"").cast('double'))

df = df.withColumn('coupon_code',lower(trim(col('coupon_code'))))

df = df.withColumn('channel',when(col('channel')=="web",'Website').when(col("channel")=="app","Mobile").otherwise(col('channel')))

# COMMAND ----------

df=df.withColumn(
    "dt",
    F.to_date("dt","yyyy-MM-dd")
)

df=df.withColumn(
    "order_ts",
    F.coalesce(
        F.to_timestamp("order_ts","yyyy-MM-dd HH:mm:ss"),
        F.to_timestamp("order_ts","dd-MM-yyyy HH:mm")
    )
)
df=df.withColumn(
    "item_seq",
    F.col("item_seq").cast("int")
)
df = df.withColumn(
    "tax_amount",
    F.regexp_replace("tax_amount", r"[^0-9.\-]", "").cast("double")
)
df=df.withColumn(
    "processed_time",F.current_timestamp()
)

# COMMAND ----------

display(df.limit(5))

# COMMAND ----------

df.write.format("delta")\
    .mode("overwrite")\
        .option("mergeSchema","true")\
            .saveAsTable(f"{catalog_name}.silver.slv_order_items")

# COMMAND ----------



# COMMAND ----------

