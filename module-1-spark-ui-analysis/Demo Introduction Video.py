# Databricks notebook source
# MAGIC %sql
# MAGIC SHOW SCHEMAS IN databricks_simulated_retail_customer_data;

# COMMAND ----------

# MAGIC %sql
# MAGIC SHOW TABLES IN databricks_simulated_retail_customer_data.v01;

# COMMAND ----------

df = spark.table(
    "databricks_simulated_retail_customer_data.v01.sales_orders"
)

df.printSchema()

# COMMAND ----------

df.count()

# COMMAND ----------

customer_counts = (
    df.groupBy("customer_id")
      .count()
      .orderBy("count", ascending=False)
)

customer_counts.show()

# COMMAND ----------

spark.conf.set("spark.sql.shuffle.partitions", 200)

heavy_shuffle = (
    df.select("customer_id", "order_number")
      .groupBy("customer_id")
      .count()
      .orderBy("count", ascending=False)
)

heavy_shuffle.collect()

# COMMAND ----------

skew_demo = (
    df.groupBy("number_of_line_items")
      .count()
      .orderBy("count", ascending=False)
)

skew_demo.show()

