# Databricks notebook source
# DBTITLE 1,Load Dataset
df = spark.table(
    "databricks_simulated_retail_customer_data.v01.sales_orders"
)

# COMMAND ----------

# DBTITLE 1,Inspect Schema
df.printSchema()

# COMMAND ----------

# DBTITLE 1,Baseline Action
df.count()

# COMMAND ----------

# DBTITLE 1,Shuffle Example #1 (Single key)
df.groupBy("customer_name").count().orderBy("count", ascending=False).show()

# COMMAND ----------

# DBTITLE 1,Shuffle Example #2 (Amplified shuffle)
df.groupBy("customer_name", "promo_info").count().orderBy("count", ascending=False).show()