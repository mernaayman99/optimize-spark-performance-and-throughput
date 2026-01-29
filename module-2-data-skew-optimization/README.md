# Module 2 – Fixing Data Skew and Shuffle Bottlenecks in Spark
# Module Overview

In this module, learners tackle one of the most common and costly Spark performance problems in real-world systems: data skew.

Using Databricks running on AWS (with guidance applicable to the Free Edition as well), learners will analyze skewed workloads generated from a realistic retail dataset. They will observe how skew manifests in Spark execution through Query Performance, Query Profile, and—when available—Spark UI metrics.

Rather than relying on executor scaling or guesswork, this module emphasizes evidence-based diagnosis and intentional skew mitigation, mirroring how Spark engineers reason about performance issues in both constrained and full-production environments.

# Learning Objectives

By the end of this module, learners will be able to:

- Explain what data skew is and why it severely degrades Spark performance
- Identify skew symptoms using execution metrics and query plans
- Understand how skew amplifies shuffle cost and creates straggler tasks
- Apply skew-mitigation techniques such as:

 - Repartitioning
 - Salting skewed keys
 - Broadcast joins (conceptual and practical considerations)
 - Adaptive Query Execution (AQE)
 - Evaluate before/after performance changes using measurable evidence
   

# Dataset Used

Databricks Marketplace – Free Dataset

Simulated Retail Customer Data

Catalog: databricks_simulated_retail_customer_data

Schema: v01

Table: sales_orders

This dataset contains naturally imbalanced customer and product activity, making it ideal for demonstrating skewed aggregations and shuffle-heavy Spark stages commonly seen in production retail analytics.

# Environment Constraints (Important)

## Primary Environment (Recorded Demos)

## Databricks Workspace linked to AWS

- General-purpose compute on AWS
- Access to Spark UI (Jobs, Stages, Executors) for deeper inspection
- Used in recorded demos to visualize skew at the executor and task level

Learner Environment (Hands-On Practice)

## ⚠️ Databricks Free Edition

Limitations:

- No standalone Spark UI tabs (Jobs / Stages / Executors)
- No custom executor sizing
- No cluster-level tuning

What learners will use instead:

- Databricks Query Performance panel
- Query Profile (logical & physical execution plans)
- Task counts, execution time, and shuffle indicators
- Controlled DataFrame transformations

This module is intentionally designed so all concepts can be learned without privileged infrastructure, while still aligning with production Spark behavior.

# Hands-On Focus
Learners will:

- Run a baseline aggregation job that exhibits data skew
- Observe performance characteristics using Query Performance metrics
- Inspect query plans to reason about uneven work distribution
- Apply one or more skew-mitigation techniques
- Compare execution metrics before and after optimization

# Key Concepts Covered

- What data skew looks like in Spark workloads
- Why skew creates straggler tasks and long-running stages
- Relationship between skew, shuffle pressure, and task imbalance
- Why adding CPU or memory does not fix skew
- Trade-offs between different mitigation strategies

# Demo Notebook 
📁 notebooks/
skew_fixing_demo.ipynb (placeholder – code used in demo)

The notebook will include:

- Baseline groupBy on a skewed key
- Query Performance inspection
- Repartitioning strategies
- Optional salting example
- Conceptual broadcast join discussion
- Before / after metrics comparison

# How Learners Analyze Skew (Step-by-Step)

# Step 1: Run the Baseline Job
Learners execute an aggregation such as:

- df.groupBy("customer_id").count()
This intentionally creates an imbalanced workload where a small number of keys dominate processing time.

# Step 2: Inspect Spark UI – Job-Level Performance

After running the baseline Spark job, learners open the Spark UI and begin analysis at the Jobs tab.

From the Jobs tab, learners observe:

- Total job duration (wall-clock time)
- Number of stages triggered by the job
- Whether the job duration exceeds expectations given the dataset size

Indicators of potential skew at the job level include:

- Job runtime disproportionately high for a moderate dataset
- One job dominating total execution time
- Delays caused by a single downstream stage

This establishes that a performance problem exists, but not yet why.

# Step 3: Inspect Spark UI – Stage & Task-Level Evidence

Learners move to the Stages tab to identify the root cause.

From the Stages tab, learners inspect:

- The slowest stage (highest duration)
- Task duration distribution within that stage
- Shuffle read and shuffle write sizes per stage

Learners then open Stage Details → Tasks to examine:

- Fastest vs slowest task durations
- Whether a small number of tasks run significantly longer
- Whether those tasks handle disproportionately large shuffle reads

Indicators of data skew include:

- One or two tasks dominating stage runtime
- Large shuffle read sizes concentrated in few tasks
- Long tail of straggler tasks delaying stage completion

This confirms skew at the task level, not a general resource shortage.

# Step 4: Inspect Spark UI – SQL & Shuffle Boundaries

Learners open the SQL tab (or SQL details linked from the job) to analyze the execution plan.

From the SQL / DAG view, learners observe:

- Where shuffle boundaries occur
- Aggregation and join operators responsible for data redistribution

Whether the shuffle originates from:

- groupBy
- join keys
- poorly aligned partitioning

This step links logical operations (groupBy, join) to physical shuffle behavior, reinforcing cause → effect reasoning.

# Step 5: Apply Skew Mitigation (Conceptual + Practical)

Based on Spark UI evidence, learners choose appropriate mitigation strategies:

- Repartitioning by a better key

Used when skew is caused by uneven partitioning

- Salting skewed keys

Used when a small number of keys dominate the dataset

- Broadcast joins

Used when one side of a join is small enough to avoid shuffle

- Adaptive Query Execution (AQE)

Used when skew varies over time or is not predictable

Learners explicitly justify why each technique fits the observed Spark UI evidence.

# Step 6: Compare Before vs After Using Spark UI

After applying the chosen optimization, learners rerun the job and compare Spark UI metrics:

From the Jobs tab:

- Reduced total runtime

From the Stages tab:

- Faster slowest stage
- More uniform task durations

From Task Details:

- Reduced gap between fastest and slowest tasks
- Lower shuffle read concentration

From the Executors tab (if available):

- More even CPU utilization
- Reduced memory pressure and GC time

# Expected Learning Outcomes
By the end of Module 2, learners should be able to:

- Confidently identify data skew using execution metrics and query plans
- Explain why skew—not compute size—is the dominant bottleneck
- Select the most appropriate mitigation strategy
- Justify optimization choices using observable evidence

# These skills directly prepare learners for:

- Module 3: SLA-Driven Spark Tuning
- Course-End Project: End-to-End Optimization

# Key Takeaway
Data skew is not a configuration problem—it’s a data problem.
This module trains learners to see skew early, diagnose it correctly, and fix it intentionally—using metrics, reasoning, and production-grade thinking rather than brute force.
