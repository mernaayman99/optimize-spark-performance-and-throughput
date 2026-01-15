# Module 3 – Tuning Spark Jobs to Meet SLA Requirements
# Module Overview

In this module, learners shift from identifying performance problems to meeting strict Service Level Agreements (SLAs). The focus is on latency-sensitive Spark workloads where execution time—not throughput alone—determines success.

Using the Databricks Free Edition, learners will evaluate Spark job execution behavior through Query Performance metrics and Query Profiles, run controlled configuration experiments at the session level, and make evidence-based tuning decisions.

This module mirrors real production scenarios where engineers must balance speed, stability, and cost, often under platform constraints.

# Learning Objectives
By the end of this module, learners will be able to:

- Define and reason about SLAs in Spark workloads
- Identify latency bottlenecks using execution metrics
- Understand how parallelism, memory pressure, and shuffle behavior affect runtime
- Perform controlled Spark tuning experiments
- Select configurations that meet SLA targets and explain trade-offs

# Dataset Used
Databricks Marketplace – Free Dataset

Simulated Retail Customer Data

Catalog: databricks_simulated_retail_customer_data

Schema: v01

Table: sales_orders

The dataset supports aggregation and join workloads suitable for SLA-driven analysis without requiring large cluster resources.

# Environment Constraints (Important)

⚠️ Databricks Free Edition Limitations

- No access to cluster sizing (executors, cores, memory)
- No Spark UI Jobs / Stages / Executors tabs
- No persistent cluster configuration

✅ What learners can tune

- Session-level Spark SQL parameters
- Partitioning strategies
- Query execution patterns
- Controlled transformations affecting shuffle behavior

All analysis is performed using:

- Databricks Query Performance panel
- Query Profile execution plans
- Wall-clock execution time

# Hands-On Focus
Learners will:

- Establish a baseline runtime that violates an SLA
- Diagnose the dominant latency bottleneck
- Apply incremental tuning changes
- Measure impact after each experiment
- Select a configuration that meets the SLA
- SLA Scenario

You are working as a Data Platform Engineer at a financial analytics company.

A Spark job that computes risk-related aggregations must complete in under 60 seconds to support downstream alerting systems. Recent runs take 80–95 seconds, causing delayed alerts and compliance risk.

You are responsible for tuning the job so it consistently meets the SLA while avoiding unnecessary resource usage.

# Key Concepts Covered

- SLA vs throughput optimization
- Why “faster” is not always “better”
- Latency amplification caused by shuffle stages
- Trade-offs between parallelism and overhead
- Cost-aware performance tuning

# Demo Notebook 
📁 notebooks/

sla_tuning_demo.ipynb (placeholder – code used in demo)

The notebook will include:
- Baseline execution
- Session-level tuning experiments
- Runtime tracking
- Query Profile inspection
- SLA validation

# How Learners Tune for SLA (Step-by-Step)
# Step 1: Establish the SLA Baseline
Learners run a baseline aggregation and record:

- Total wall-clock runtime
- Rows read
- Query execution time
- Task count
- The result fails the SLA.

# Step 2: Inspect Query Performance
From “Show performance”, learners analyze:

- Execution vs optimization time
- Long-running operations
- Query latency breakdown
- They identify whether the delay is caused by:
- Excessive shuffle
- Under-parallelization
- Inefficient partitioning

# Step 3: Examine Query Profile
Learners open Query Profile to:

- Locate shuffle boundaries
- Inspect aggregation stages
- Identify plan inefficiencies
- This replaces traditional Spark Stage analysis.

# Step 4: Run Controlled Tuning Experiments
Learners modify one variable at a time, such as:

- spark.sql.shuffle.partitions
- Repartition strategy
- Aggregation order
- Data reduction before shuffle

Each change is evaluated independently.

# Step 5: Compare Results Against SLA
Learners create a comparison:		

| Configuration| Runtime  | SLA Met  |
|----------    |----------|----------|
| Baseline     | 92s      | ❌ No    |
|Experiment 1  | 68s      |❌ No     |
|Experiment 2  | 54s      |❌ No     |



# By the end of Module 3, learners will be able to:

- Tune Spark jobs with SLA goals in mind
- Defend configuration choices using metrics
- Avoid over-provisioning as a default solution
- Think like production-focused Spark engineers

# Key Takeaway

Meeting an SLA is not about making Spark “as fast as possible.”
It is about making it predictably fast enough—with evidence, control, and discipline.

# How This Module Feeds the Course-End Project

Module 3 completes the skill set required for the End-to-End Spark Optimization Project, where learners must:

- Diagnose bottlenecks (Module 1)
- Fix data skew and shuffle issues (Module 2)
- Tune configurations to meet an SLA (Module 3)
