# Databricks notebook source
# DBTITLE 1,Load Dataset
df = spark.table(
    "databricks_simulated_retail_customer_data.v01.sales_orders"
)

# COMMAND ----------

# DBTITLE 1,Inspect Baseline Partition Count
# df.rdd.getNumPartitions()
df.explain(mode="formatted")

# COMMAND ----------

# DBTITLE 1,Cache Dataset for Stable Measurements
df.cache()
df.count()

# COMMAND ----------

# DBTITLE 1,Baseline Aggregation (SLA Violation)
baseline = (
    df.groupBy("customer_id")
      .count()
      .orderBy("count", ascending=False)
)

baseline.show()


# COMMAND ----------

# DBTITLE 1,Inspect Shuffle Partition Configuration
spark.conf.get("spark.sql.shuffle.partitions")

# COMMAND ----------

# DBTITLE 1,Tune Shuffle Partitions
spark.conf.set("spark.sql.shuffle.partitions", "32")


# COMMAND ----------

# DBTITLE 1,Increase Executor Memory
# spark.conf.set("spark.executor.memory", "6g")

# COMMAND ----------

# DBTITLE 1,Tune Cores per Executor
# spark.conf.set("spark.executor.cores", "2")

# COMMAND ----------

# DBTITLE 1,Explicit Repartitioning
df_tuned = df.repartition(32, "customer_id")

# COMMAND ----------

# DBTITLE 1,Rerun Job with Tuned Configuration
tuned = (
    df_tuned.groupBy("customer_id")
            .count()
            .orderBy("count", ascending=False)
)

tuned.show()
