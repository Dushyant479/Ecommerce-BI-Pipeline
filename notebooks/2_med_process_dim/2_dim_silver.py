# Databricks notebook source
from pyspark.sql.types import *
import pyspark.sql.functions as F

catalog_name = 'ecommerce'

# COMMAND ----------

# MAGIC %md
# MAGIC #Brands

# COMMAND ----------

df_bronze = spark.read.table("ecommerce.bronze.brz_brands")
display(df_bronze)

# COMMAND ----------

df_silver = df_bronze.withColumn("brand_name",F.trim(F.col("brand_name")))
df_silver.show(10)

# COMMAND ----------

df_silver = df_silver.withColumn("brand_code",F.regexp_replace(F.col("brand_code"),r'[^A-Za-z0-9]',''))
df_silver.show(10)


# COMMAND ----------

df_silver.select("category_code").distinct().show()

# COMMAND ----------

anomalies= {
    "GROCERY":"GRCY",
    "BOOKS":"BKS",
    "TOYS":"TOY"
}
df_silver = df_silver.replace(to_replace=anomalies, subset = ["category_code"])
df_silver.select("category_code").distinct().show()

# COMMAND ----------

df_silver.write.format("delta").mode("overwrite").option("mergeSchema","true").saveAsTable(f"{catalog_name}.silver.slv_brands")

# COMMAND ----------

# MAGIC %md
# MAGIC #Category

# COMMAND ----------

df_bronze=spark.table(f"{catalog_name}.bronze.brz_category")
df_bronze.show(10)

# COMMAND ----------

df_duplicates = df_bronze.groupBy("category_code").count().filter(F.col("count")>1)
display(df_duplicates)

# COMMAND ----------

df_silver = df_bronze.dropDuplicates(["category_code"])
display(df_silver)

# COMMAND ----------

df_silver = df_silver.withColumn("category_code",F.upper(F.col("category_code")))
display(df_silver)

# COMMAND ----------

df_silver.write.format("delta").mode("overwrite").option("mergeSchema","true").saveAsTable(f"{catalog_name}.silver.slv_category")

# COMMAND ----------

# MAGIC %md
# MAGIC #Products
# MAGIC

# COMMAND ----------

df_bronze = spark.read.table(f"{catalog_name}.bronze.brz_products")
display(df_bronze)

# COMMAND ----------

row_count, column_count = df_bronze.count(), len (df_bronze.columns)
print(f"Row count: {row_count}, Column count: {column_count}")

# COMMAND ----------

df_bronze.select("weight_grams").show(5,truncate=False)

# COMMAND ----------

df_silver = df_bronze.withColumn("weight_grams",F.trim(F.regexp_replace(F.col("weight_grams"),"g","").cast(IntegerType())))

# COMMAND ----------

df_silver.select("weight_grams").show(5)

# COMMAND ----------

df_silver.select('length_cm').show(5)

# COMMAND ----------

df_silver = df_silver.withColumn(
    "length_cm",
    F.regexp_replace(F.col("length_cm"),",",".").cast(FloatType())
)
df_silver.select("length_cm").show(3)

# COMMAND ----------

df_silver.select("material").distinct().show()

# COMMAND ----------

df_silver = df_silver.withColumn("category_code",
                                 F.upper(F.col("category_code"))
                                 ).withColumn(
                                     "brand_code",
                                     F.upper(F.col("brand_code"))
                                 )
df_silver.select("category_code","brand_code").show(2)

# COMMAND ----------

df_silver = df_silver.withColumn(
    "material",
    F.when(F.col("material") == "Coton","Cotton")
        .when(F.col("material") == "Alumium", "Aluminium")
        .when(F.col("material") == "Ruber","Rubber")
        .otherwise(F.col("material"))
)
 
df_silver.select("material").distinct().show()

# COMMAND ----------

df_silver.filter(F.col('rating_count') < 0).select("rating_count").show(3)

# COMMAND ----------

#convert negative rating_count to positive
df_silver = df_silver.withColumn(
    "rating_count",
    F.when(F.col("rating_count").isNotNull(),F.abs(F.col("rating_count")))
    .otherwise(F.lit(0)) # if null replace it with 0
)
display(df_silver)

# COMMAND ----------

df_silver.write.format("delta").mode("overwrite").option("mergeSchema","true").saveAsTable(f"{catalog_name}.silver.slv_products")

# COMMAND ----------

# MAGIC %md
# MAGIC #Customers

# COMMAND ----------

df_bronze= spark.read.table(f"{catalog_name}.bronze.brz_customers")

row_count,column_count = df_bronze.count(), len(df_bronze.columns)

print(f"Row count: {row_count}")
print(f"Column count: {column_count}")

df_bronze.show(10)

# COMMAND ----------

null_count= df_bronze.filter(F.col("customer_id").isNull()).count()
null_count

# COMMAND ----------

df_silver = df_bronze.dropna(subset=["customer_id"])
row_count = df_silver.count()
print(f"Row count after dropping null values: {row_count}")

# COMMAND ----------

null_count = df_silver.filter(F.col("phone").isNull()).count()
print(f"Number of nulls in phone: {null_count}")

# COMMAND ----------

df_silver = df_silver.fillna("Not Available",subset=["phone"])
df_silver.filter(F.col("phone").isNull()).show()

# COMMAND ----------

df_silver.write.format("delta").mode("overwrite").option("mergeSchema","true").saveAsTable(f"{catalog_name}.silver.slv_customers")

# COMMAND ----------

# MAGIC %md
# MAGIC #Calendar

# COMMAND ----------

df_bronze = spark.read.table(f"{catalog_name}.bronze.brz_date")

row_count,column_count  =df_bronze.count(), len(df_bronze.columns)

print(f"Row count: {row_count}")
print(f"Column count: {column_count}")
df_bronze.show(3)

# COMMAND ----------

df_bronze.printSchema()

# COMMAND ----------

#Converting string to date
from pyspark.sql.functions import to_date

df_silver = df_bronze.withColumn("date",to_date(df_bronze["date"],"dd-MM-yyyy"))

# COMMAND ----------

print(df_silver.printSchema())

# COMMAND ----------

duplicates = df_silver.groupBy('date').count().filter("count > 1")
print("Total duplicated Rows: ",duplicates.count())
display(duplicates)

# COMMAND ----------

df_silver = df_silver.dropDuplicates(['date'])
row_count = df_silver.count()
print("Rows After removing Duplicates: ",row_count)

# COMMAND ----------

#Capitalize first letter of each word in day_name
df_silver = df_silver.withColumn("day_name",F.initcap(F.col("day_name")))
df_silver.show(5)

# COMMAND ----------

df_silver = df_silver.withColumn("week_of_year",F.abs(F.col("week_of_year")))
df_silver.show(3)

# COMMAND ----------

df_silver = df_silver.withColumn("quarter",F.concat_ws("",F.concat(F.lit("Q"),F.col("quarter"),F.lit("-"),F.col("year"))))
df_silver= df_silver.withColumn("week_of_year",F.concat_ws("-",F.concat(F.lit("Week"),F.col("week_of_year"),F.lit("-"),F.col("year"))))

df_silver.show()

# COMMAND ----------

df_silver= df_silver.withColumnRenamed("week_of_year","week")

# COMMAND ----------

df_silver.write.format("delta").mode("overwrite").option("mergeSchema","true").saveAsTable(f"{catalog_name}.silver.slv_calendar")

# COMMAND ----------

