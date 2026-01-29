# Module 1 – Analyzing Spark Job Performance Using Databricks Query Profiles
# Module Overview

In this module, learners are introduced to Spark performance analysis fundamentals using Databricks linked to AWS.
The focus is on understanding how Spark jobs execute at runtime and how performance bottlenecks can be identified using evidence-based metrics, not assumptions.

Depending on the Databricks account type:

- Paid Databricks (AWS-backed) exposes the full Spark UI
- Databricks Free Edition exposes Query Performance and Query Profile views

This module is intentionally designed so that both environments are supported, while emphasizing production-relevant Spark UI analysis.

# Learning Objectives
By the end of this module, learners will be able to:

- Inspect Spark execution behavior using Spark UI and Databricks execution metrics
- Interpret task duration, shuffle I/O, and execution timing
- Identify early indicators of shuffle overhead and parallelism imbalance
- Explain why similar Spark operations can produce different performance outcomes
- Build the analytical foundation required for SLA-driven tuning in later modules

# Dataset Used
Databricks Marketplace – Free Dataset

Simulated Retail Customer Data

Catalog: databricks_simulated_retail_customer_data

Schema: v01

Table: sales_orders

This dataset represents fictional retail transactions and is commonly used to simulate real-world analytical workloads involving grouping, aggregation, and shuffling.

The dataset is compatible with:

- Databricks Free Edition (serverless)
- Paid Databricks workspaces linked to AWS

# Environment & Platform Context (Important)
## Databricks on AWS (Primary Demo Environment)

The recorded demos in this module use:

- Databricks workspace linked to AWS
- General-purpose cluster

Full Spark UI access, including:

- Jobs tab
- Stages tab
- Task details
- Shuffle metrics
- Executors tab

This reflects real production environments where Spark performance tuning is performed.

## Databricks Free Edition (Learner-Friendly Option)

Learners using the Databricks Free Edition can still follow along using:

- Serverless Spark execution
- Query Performance summary
- Query Profile view (logical & physical plan)
- Execution timing, task count, and shuffle indicators

While the classic Spark UI tabs are not exposed in Free Edition, the same execution signals are still observable through Databricks-provided performance tooling.

# Hands-On Focus
This module trains learners to analyze Spark performance using metrics and execution evidence.

Learners will observe:

- Total wall-clock execution time
- Task count and parallelism
- Rows read and bytes read
- Indicators of shuffle operations
- Execution time vs optimization time
- How query structure affects performance

# Demo Notebook

📁 notebooks/

spark_ui_analysis_demo.ipynb (placeholder – code used in demo)

# The notebook will include:

-Loading the retail dataset
- Inspecting schema and baseline execution behavior
- Running aggregation workloads
- Introducing shuffle-heavy operations
- Comparing execution metrics across runs
- Navigating Spark UI or Query Profile (depending on environment)

# How Learners Analyze Performance (Step-by-Step)

# Step 1: Execute a Spark Job
Learners execute a Spark DataFrame operation such as:

- groupBy
- count
- orderBy

This triggers Spark execution in the Databricks backend.

# Step 2: Inspect Execution Metrics
Depending on the environment:

### On Databricks (AWS-linked)

Learners navigate:

- Spark UI → Jobs tab
- Spark UI → Stages tab
- Task duration and shuffle metrics
- Executors resource utilization

### On Databricks Free Edition

Learners use:

- “Show performance” panel
- Query Performance summary
- Query Profile view

# Step 3: Analyze Execution Behavior
Learners identify:

- Where time is spent (execution vs optimization)
- Evidence of shuffle operations
- Task duration imbalance
- Signals of limited parallelism

This analysis replaces guesswork with metrics-driven reasoning.

# Expected Learning Outcomes
By the end of Module 1, learners should be able to explain:

- Why Spark job runtime is often dominated by execution rather than planning
- How grouping operations introduce shuffle overhead
- Why task count and partitioning affect parallelism
- How performance issues can be detected early—before SLA violations occur

Module 1 establishes the observability mindset required for Spark performance engineering.

# This prepares learners for:

- Module 2: Data Skew Optimization
- Module 3: SLA-Driven Tuning
- Course-End Project: End-to-End Optimization

# Key Takeaway
Spark performance leaves observable signals in every execution.

Whether through Spark UI or Databricks Query Profiles, this module trains learners to read those signals, validate assumptions, and reason about performance like a production Spark engineer.
