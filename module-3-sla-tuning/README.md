# Module 3 – Tuning Spark Jobs to Meet SLA Requirements
# Module Overview

In this module, learners move from diagnosing Spark performance issues to actively tuning Spark jobs to meet strict Service Level Agreements (SLAs).

The focus is on latency-sensitive workloads, where end-to-end execution time determines success—not throughput alone.

This module uses a Databricks workspace linked to AWS, allowing learners to work with the full Spark UI (Jobs, Stages, Executors, SQL tabs) and perform evidence-based tuning using real execution metrics.

Learners practice the same workflow used by production Spark engineers:
observe → hypothesize → tune → validate against SLA.

⚠️ Learners using Databricks Free Edition can still follow the tuning logic conceptually using Query Performance and Query Profile, but the primary demonstrations in this module rely on Spark UI.

# Learning Objectives
By the end of this module, learners will be able to:

- Define and reason about SLAs in Spark workloads
- Identify latency bottlenecks using Spark UI metrics
- Interpret task duration, shuffle I/O, executor CPU and memory usage
- Understand how parallelism, memory pressure, and shuffle behavior affect runtime
- Perform controlled Spark tuning experiments
- Select configurations that meet SLA targets and justify trade-offs

# Dataset Used
Databricks Marketplace – Free Dataset

Simulated Retail Customer Data

Catalog: databricks_simulated_retail_customer_data

Schema: v01

Table: sales_orders

This dataset supports realistic aggregation and shuffle-heavy workloads suitable for SLA-driven tuning without requiring large clusters.

# Environment Constraints (Important)

Primary Environment (Used in Demo)

✅ Databricks workspace linked to AWS

✅ Full Spark UI access:

- Jobs tab
- Stages tab
- Task details
- Shuffle metrics
- Executors tab

✅ Ability to:

- Modify Spark configurations at session or cluster level
- Observe executor-level CPU, memory, and GC behavior

Free Edition Note (For Learners)

⚠️ Databricks Free Edition limitations:

- No full Spark UI (Jobs / Stages / Executors)
- No cluster-level executor tuning

Learners on Free Edition can still:

- Follow the tuning logic
- Use Query Performance and Query Profile
- Observe wall-clock runtime and execution plan changes

# Hands-On Focus

Learners will:

- Establish a baseline runtime that violates an SLA
- Identify the dominant latency bottleneck using Spark UI
- Run controlled tuning experiments
- Measure performance impact after each change
- Validate whether the SLA is met
- Explain trade-offs between performance, stability, and cost

SLA Scenario

You are working as a Data Platform Engineer at a financial analytics company.

A Spark job that computes risk-related aggregations must complete in under 60 seconds to support downstream alerting systems.

Recent runs take 80–95 seconds, causing delayed alerts and compliance risk.

Your task is to tune the job so it consistently meets the SLA, without unnecessary over-provisioning.

# Key Concepts Covered

- SLA vs throughput optimization
- Why reducing shuffle latency is often the fastest win
- How stage-level delays amplify end-to-end latency
- Executor underutilization vs memory pressure
- Cost-aware tuning decisions
- Evidence-based performance validation

# Demo Notebook 
📁 notebooks/

sla_tuning_demo.ipynb (placeholder – code used in demo)

The notebook will include:
- Baseline execution
- Spark UI inspection (Jobs, Stages, Executors)
- Controlled tuning experiments
- Runtime comparison
- SLA validation

# How Learners Tune for SLA (Step-by-Step)
# Step 1: Establish the SLA Baseline

Learners run a baseline aggregation and record:

- Total job runtime (Jobs tab)
- Slowest stage duration (Stages tab)
- Maximum task duration
- Shuffle read/write size
- Executor CPU and memory utilization

➡️ Result: SLA violation confirmed.
# Step 2: Identify the Latency Bottleneck

Using Spark UI, learners inspect:

- Jobs tab → total runtime
- Stages tab → longest-running stage
- Task details → straggler tasks
- Shuffle metrics → heavy shuffle stages
- Executors tab → CPU imbalance, GC time, memory pressure

Learners determine whether the delay is caused by:

- Excessive shuffle
- Poor parallelism
- Memory pressure
- Executor imbalance

# Step 3: Run Controlled Tuning Experiments

Learners change one variable at a time, such as:

- spark.sql.shuffle.partitions
- Repartitioning strategy
- Executor memory
- Cores per executor

Each experiment is evaluated independently.

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

Spark UI metrics are used as evidence—not assumptions.

# By the end of Module 3, learners will be able to:

-Tune Spark jobs with SLA goals in mind
- Identify which configuration changes actually matter
- Defend tuning decisions using Spark UI metrics
- Avoid blindly adding resources
- Think like production-focused Spark engineers

# Key Takeaway

Meeting an SLA is not about making Spark “as fast as possible.”

It’s about making it predictably fast enough, using:

- Evidence
- Controlled experiments
- Clear trade-off analysis

# How This Module Feeds the Course-End Project

Module 3 completes the skill set required for the End-to-End Spark Optimization Project, where learners must:

- Diagnose bottlenecks (Module 1)
- Fix data skew and shuffle issues (Module 2)
- Tune configurations to meet an SLA (Module 3)
