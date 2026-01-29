# Databricks notebook source
# DBTITLE 1,Confirm AQE Is Enabled (Baseline Check)
spark.conf.get("spark.sql.adaptive.enabled", "true")

# COMMAND ----------

# DBTITLE 1,Load Dataset
df = spark.table(
    "databricks_simulated_retail_customer_data.v01.sales_orders"
)

# COMMAND ----------

# DBTITLE 1,Baseline Aggregation (Shuffle Without Join)
df.groupBy("promo_info").count().show()

# COMMAND ----------

# DBTITLE 1,Join Without Explicit Optimization (AQE Opportunity)
customers = df.select(
    "customer_id", "customer_name"
).distinct()

orders = df.select(
    "customer_id", "promo_info", "number_of_line_items"
)

joined_df = orders.join(customers, "customer_id")
joined_df.show()


# COMMAND ----------

# DBTITLE 1,Join + Aggregation (AQE Fully Engaged)
join_agg = (
    orders.join(customers, "customer_id")
          .groupBy("promo_info")
          .count()
)

join_agg.show()


# COMMAND ----------

# DBTITLE 1,Skew-Prone Column (AQE Assist Scenario)
df.groupBy("customer_name").count().show()