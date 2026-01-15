# Module 1 – Analyzing Spark Job Performance Using Databricks Query Profiles#
# Module Overview

In this module, learners are introduced to Spark performance analysis fundamentals using the Databricks Free Edition.
Because the free tier does not expose the full standalone Spark UI (Jobs, Stages, Executors tabs), learners will instead analyze real Spark execution behavior through:

Databricks Query Performance panel
Query Profile view
Execution metrics surfaced directly in the notebook UI

This module builds the analytical mindset required to diagnose Spark performance issues using metrics and evidence, even in constrained environments.

# Learning Objectives
By the end of this module, learners will be able to:
Understand how Spark jobs execute at runtime
Interpret Databricks Query Performance metrics
Identify early indicators of shuffle overhead and task parallelism
Explain why seemingly simple Spark operations can behave differently
Prepare for deeper Spark UI analysis in later modules and real-world clusters

# Dataset Used
Databricks Marketplace – Free Dataset
Simulated Retail Customer Data
Catalog: databricks_simulated_retail_customer_data
Schema: v01
Table: sales_orders
This dataset represents fictional retail transactions and is optimized for use in Databricks Free Edition without requiring cluster creation.

# Environment Constraints (Important)
⚠️ Databricks Free Edition Limitations
Full Spark UI (Jobs / Stages / Executors tabs) is not available
No custom cluster configuration
No executor-level tuning

✅ What is available and used in this module
Serverless Spark execution
Query Performance summary
Query Profile (logical & physical execution view)
Execution timing, task count, shuffle indicators
This module is intentionally designed to work within these constraints.

# Hands-On Focus
Learners will analyze Spark behavior using Databricks Query Performance, not raw Spark UI tabs.
What Learners Will Observe
From the notebook output and Query Profile, learners will examine:
Total wall-clock execution time
Number of tasks executed
Rows read and bytes read
Shuffle-related indicators
Execution vs optimization time split
Impact of repartitioning and grouping operations

# Demo Notebook

📁 notebooks/

spark_ui_analysis_demo.ipynb (placeholder – code used in demo)

# The notebook will include:

Reading from the retail dataset
A baseline aggregation job
A repartitioned version of the same job
Query Performance comparison

# How Learners Analyze Performance (Step-by-Step)

# Step 1: Run the Query
Learners execute a Spark DataFrame operation such as:
groupBy
count
orderBy
This triggers Spark execution in the Databricks backend.

# Step 2: Open Query Performance Panel
After execution:
Expand “Show performance”
Observe:
Total wall-clock duration
Tasks completed
Rows read
Bytes read

# Step 3: Open Query Profile
Learners click “See query profile” to inspect:
Execution plan stages
Time spent executing vs optimizing
Physical operations (scan, shuffle, aggregation)
Evidence of parallelism and shuffle
This substitutes for:
Spark Jobs tab
Spark Stages tab
Spark SQL tab

# Expected Learning Outcomes
By the end of Module 1, learners should be able to explain:
Why a Spark job’s runtime is dominated by execution vs optimization
How grouping operations trigger shuffles
Why task count matters for parallelism
How Spark performance issues can be detected before full UI access

# This prepares learners for:
Module 2: Data Skew Optimization
Module 3: SLA-Driven Tuning
Course-End Project: End-to-End Optimization
