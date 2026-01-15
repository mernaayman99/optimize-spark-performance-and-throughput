# Module 2 – Fixing Data Skew and Shuffle Bottlenecks in Spark

# Module Overview
In this module, learners focus on one of the most common and damaging Spark performance problems: data skew.
Using the Databricks Free Edition, learners will simulate skewed workloads, observe their performance impact through Databricks Query Performance and Query Profile, and apply practical skew-mitigation techniques.
While full Spark UI tabs (Stages, Executors) are not available in the free tier, learners will still diagnose skew using execution metrics, task counts, and query plans—mirroring how engineers reason about skew in constrained environments.

# Learning Objectives
By the end of this module, learners will be able to:
Explain what data skew is and why it degrades Spark performance
Identify skew symptoms using Query Performance metrics
Understand how skew affects shuffle operations and task parallelism
Apply skew-mitigation techniques such as:
Repartitioning
Salting keys
Broadcast joins (conceptually and where applicable)
Evaluate before/after performance changes using metrics

# Dataset Used
Databricks Marketplace – Free Dataset
Simulated Retail Customer Data
Catalog: databricks_simulated_retail_customer_data
Schema: v01
Table: sales_orders
This dataset naturally contains imbalanced customer activity, making it ideal for demonstrating skewed aggregations (e.g., some customers generate far more orders than others).

# Environment Constraints (Important)
⚠️ Databricks Free Edition Limitations
No access to full Spark UI (Jobs / Stages / Executors)
No custom executor sizing
No cluster-level tuning

✅ What is used instead
Databricks Query Performance panel
Query Profile execution plans
Task counts, execution time, shuffle indicators
Controlled DataFrame transformations
This module is intentionally designed to teach skew concepts without relying on privileged infrastructure.

# Hands-On Focus
Learners will:
Run a baseline aggregation job that exhibits skew
Observe performance characteristics using Query Performance
Apply skew-mitigation techniques
Compare before/after execution metrics

# Key Concepts Covered
What data skew looks like in Spark
Why skew creates “straggler” tasks
Relationship between skew and shuffle pressure
Why adding resources alone does not fix skew
Trade-offs of different mitigation strategies

# Demo Notebook (Code Added Later)
📁 notebooks/
skew_fixing_demo.ipynb (placeholder – code provideded)
The notebook will include:
Baseline groupBy on a skewed key
Query Performance inspection
Repartitioning by key
Optional salting example
Metrics comparison

# How Learners Analyze Skew (Step-by-Step)
# Step 1: Run the Baseline Job
Learners execute an aggregation such as:
groupBy(customer_id).count()
This intentionally creates an imbalanced workload.

# Step 2: Inspect Query Performance
From “Show performance”, learners observe:
Total execution time
Number of tasks
Rows read
Bytes read
Execution vs optimization time
Signs of skew include:
High execution time relative to data size
Many tasks for small datasets
Inefficient execution despite serverless compute

# Step 3: Open Query Profile
Learners click “See query profile” to inspect:
Physical execution stages
Shuffle boundaries
Aggregation behavior
Evidence of uneven work distribution
This substitutes for Spark Stage Details.

# Step 4: Apply Skew Mitigation
Learners apply one or more techniques:
Repartition by key
Increase partition count
(Conceptually) discuss salting and broadcast joins

# Step 5: Compare Before vs After
Learners compare:
Runtime
Task count
Execution time distribution
Overall efficiency

# Expected Learning Outcomes
By the end of Module 2, learners should be able to:
Confidently identify data skew without executor-level metrics
Explain why skew dominates job runtime
Choose appropriate mitigation techniques
Justify optimizations using observable metrics

# These skills directly prepare learners for:
Module 3: SLA-Driven Spark Tuning
Course-End Project: End-to-End Optimization

# Key Takeaway
Data skew is not a configuration problem—it’s a data problem.
This module trains learners to see skew early, diagnose it correctly, and fix it with intent rather than brute force.
