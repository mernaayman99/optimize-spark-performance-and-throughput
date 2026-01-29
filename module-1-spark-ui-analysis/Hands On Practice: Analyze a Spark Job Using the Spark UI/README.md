# Hands-On Practice – Module 1
# Analyze a Spark Job Using the Spark UI

## REFERENCE SOLUTION
### Scenario Recap

DataWave Analytics experienced SLA delays in a nightly Spark ETL job processing retail transactions.
The job, built on the Simulated Retail Customer Data, shows signs of:

- Slow stages
- Uneven task durations
- Heavy shuffle activity
- Inefficient executor utilization

The objective is to analyze Spark UI metrics, identify performance bottlenecks, and recommend targeted optimizations.

### Dataset Used

Databricks Marketplace – Free Dataset
Catalog: databricks_simulated_retail_customer_data
Schema: v01
Table: sales_orders

This dataset generates realistic shuffle-heavy Spark workloads suitable for performance analysis.

## Activity 1: Inspect Job and Stage Performance (10 minutes)
#### Step 1: Identify the Slowest Job

Spark UI → Jobs Tab

Observed Metrics
- Total job duration: ~... seconds
- Multiple stages triggered by aggregation
- One job dominates overall runtime

Finding

- The job exceeds its expected SLA window.

#### Step 2: Examine Stage-Level Performance

Spark UI → Stages Tab

Observed Metrics

- One shuffle-heavy stage consumes the majority of execution time
- Stage duration significantly higher than others
- High task count with uneven completion times

Finding

Performance is dominated by a single expensive shuffle stage.

#### Step 3: Analyze Shuffle Behavior

Spark UI → Stage Details

Observed Metrics

- Large shuffle read/write sizes
- Shuffle activity concentrated in a subset of tasks
- Some tasks process far more data than others

Finding

Shuffle amplification and task imbalance are key contributors to slowdown.

#### ✅ Expected Output (Activity 1)

Identification of:

- The slowest job
- The longest-running stage
- Evidence of shuffle pressure and task imbalance

#### 💡 Tips

- Focus on which stage dominates total runtime, not just task count.
- Large shuffle sizes combined with uneven task durations often indicate suboptimal partitioning.
- A single slow stage is usually the best optimization target.

## Activity 2: Analyze Executor Behavior (10 minutes)
#### Step 1: Review Executor Memory Usage

Spark UI → Executors Tab

Observed Metrics

- Executors show high memory usage during shuffle stages
- Evidence of spill-to-disk events
- Increased garbage collection (GC) time

Finding

Memory pressure contributes to execution instability and latency.

#### Step 2: Inspect Task Distribution Across Executors

Observed Metrics

- Some executors process significantly more tasks than others
- Idle executors observed while others remain busy

Finding

Poor workload distribution reduces effective parallelism.

#### Step 3: Observe CPU and GC Behavior

Observed Metrics

- Uneven CPU utilization
- Executors spending time in GC instead of processing tasks

Finding

Resource imbalance limits throughput and delays job completion.

#### ✅ Expected Output (Activity 2)

Clear explanation of whether:

- Memory pressure
- Executor imbalance
- GC overhead

are contributing to performance degradation.

#### 💡 Tips

- High GC time often correlates with shuffle-heavy stages.
- Idle executors indicate insufficient or misaligned parallelism.
- Executor imbalance is frequently caused by skewed partitions.

## Compile Your Findings
#### Requirement 1: Spark Job Bottleneck Analysis

- Identified Bottlenecks
- Shuffle-Heavy Stage

  Evidence: Large shuffle read/write sizes

  Impact: Dominates job runtime

- Task Duration Imbalance

  Evidence: Wide spread between fastest and slowest tasks

  Impact: Straggler tasks delay stage completion

- Executor Resource Inefficiency

  Evidence: Uneven CPU usage, elevated GC time
  
  Impact: Reduced throughput and higher latency

#### Requirement 2: Optimization Recommendations
- Bottleneck	Recommendation	Rationale
- Heavy shuffle	Repartition data on aggregation key	Improves data distribution
- Task skew	Enable Adaptive Query Execution (AQE)	Dynamically mitigates skew
- Executor imbalance	Tune shuffle partition count	Reduces overhead and improves parallelism

#### Requirement 3: Summary Assessment (≈180 words)

The primary performance bottleneck in this Spark job is a shuffle-heavy aggregation stage with uneven task durations. Spark UI metrics clearly show that a small number of tasks dominate execution time, indicating data skew and inefficient partitioning. This imbalance causes executor underutilization, elevated memory pressure, and increased garbage collection overhead, ultimately leading to SLA violations.

Targeted optimizations should focus on reducing shuffle cost and improving parallelism. Repartitioning the dataset on the aggregation key would distribute workload more evenly across tasks. Enabling Adaptive Query Execution would allow Spark to dynamically adjust partition sizes and mitigate skew at runtime. Additionally, tuning the shuffle partition count to better match dataset size and available executors can reduce scheduling overhead and stabilize execution.

By applying these optimizations, the job would achieve more balanced task execution, improved executor utilization, and reduced latency—bringing the pipeline back within SLA limits. This analysis demonstrates how Spark UI metrics provide concrete, actionable evidence for diagnosing and resolving performance issues in real-world production workloads.

## Key Takeaway

Spark performance tuning is driven by evidence, not assumptions.
By systematically inspecting Spark UI metrics—jobs, stages, tasks, and executors—engineers can identify true bottlenecks and apply targeted optimizations that restore SLA compliance.
