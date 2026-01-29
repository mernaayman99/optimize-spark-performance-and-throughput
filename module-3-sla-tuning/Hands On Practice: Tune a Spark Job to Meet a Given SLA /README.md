# Hands-On Practice – Module 3
# Partitioning & SLA-Driven Spark Job Tuning

## REFERENCE SOLUTION
### Scenario Recap
After identifying shuffle bottlenecks (Module 1) and correcting skew using AQE and join optimizations (Module 2), DataWave Analytics still faces strict SLA requirements.

The business requires that nightly aggregation jobs:

- Complete within a fixed time window
- Avoid executor memory pressure
- Scale predictably as data volume grows

Your task in this module is to tune Spark execution parameters and partitioning strategies using Spark UI evidence, then verify whether the job meets its SLA.

### Dataset Used

Databricks Marketplace – Free Dataset

Catalog: databricks_simulated_retail_customer_data
Schema: v01
Table: sales_orders

This dataset simulates a real production analytics workload with enough volume to expose partitioning and executor inefficiencies.

## Activity 1: Baseline Job & SLA Violation (5 minutes)
#### Step 1: Run Baseline Aggregation

- Spark Operation
- Group orders by customer_id
- Count transactions
- Sort by frequency

Observed Spark UI Metrics

- Job runtime exceeds SLA threshold
- One shuffle stage dominates execution
- Task durations vary significantly

#### Step 2: Inspect Spark UI – Baseline

Spark UI → Jobs Tab

- Total runtime exceeds SLA
- Job completion delayed


Spark UI → Stages Tab

- One stage consumes the majority of runtime
- Large number of shuffle tasks


Spark UI → Task Details

- Long tail of straggler tasks
- High variance between fastest and slowest tasks


Spark UI → Executors Tab

- Uneven CPU utilization
- Elevated GC time
- Memory pressure visible

#### Expected Output (Activity 1)

Clear confirmation that:

- The job violates SLA
- Partitioning and resource allocation are contributing factors


#### 💡 Tips

- SLA issues usually appear first at the stage level
- Long GC time indicates memory pressure, not compute shortage
- Task skew delays the entire job

## Activity 2: Partitioning & Parallelism Optimization (5 minutes)

#### ⚠️ Important Constraint

- Executor memory and cores cannot be modified at runtime in Databricks shared clusters.
- Tuning is demonstrated through partition strategy and shuffle configuration, validated via Spark UI.

#### Step 1: Inspect Shuffle Partition Configuration

Observed

- Default shuffle partition count is high relative to data size

Impact

- Excessive task scheduling overhead
- Increased shuffle cost

#### Step 2: Tune Shuffle Partitions

Action

- Reduce spark.sql.shuffle.partitions to align with executor capacity

Observed Spark UI Metrics

- Fewer shuffle tasks
- Reduced stage duration
- Improved task efficiency

#### Step 3: Explicit Repartitioning by Aggregation Key
Action

- Repartition dataset by customer_id before aggregation

Observed Spark UI Metrics

- More uniform task durations
- Reduced skew
- Faster stage completion

#### Expected Output (Activity 2)

Evidence that:

- Shuffle stages complete faster
- Task duration variance decreases
- Parallelism is better aligned with cluster resources


#### 💡 Tips

- Partitioning is the most controllable tuning lever in shared clusters
- Always repartition on keys used in groupBy
- Optimal partition counts balance overhead and parallelism

## Activity 3: Post-Tuning SLA Validation (10 minutes)

#### Step 1: Rerun the Optimized Job

Observed Improvements

- Total runtime reduced
- Slowest stage duration significantly lower
- No extreme straggler tasks

#### Step 2: Validate via Spark UI

Spark UI → Jobs Tab

- Runtime now within SLA target

Spark UI → Stages Tab

- Reduced shuffle stage dominance
- Balanced execution times

Spark UI → Executors Tab

- More even CPU usage
- Lower GC overhead
- Stable memory utilization

#### Expected Output (Activity 3)

Confirmation that:

- Job now meets SLA
- Resource usage is healthier
- Execution is more predictable

#### 💡 Tips

- SLA tuning is iterative, not one-time
- Spark UI is the source of truth for tuning decisions
- Healthy executors show consistent CPU and low GC

## Compile Your Findings
#### Requirement 1: Baseline SLA Metrics

Baseline Performance Snapshot (Before Tuning)

Using the Spark UI (Jobs, Stages, Executors tabs) and execution metrics from the Simulated Retail Customer Data workload, the following baseline metrics were observed:

- Baseline Metrics Collected
- Total Runtime: ~... seconds 
- Slowest Stage Duration: ~... seconds
- Maximum Task Duration: ~... seconds

Shuffle Read / Write:

- Shuffle Read: High (hundreds of MB concentrated in one stage)
- Shuffle Write: Moderate but uneven across tasks

Executor Utilization:

- CPU usage uneven (some executors idle while others overloaded)
- Memory pressure visible through increased GC time
- Occasional spill-to-disk events during shuffle-heavy stages

Interpretation

- The job violates the SLA requirement of < 60 seconds.
- Performance issues are not caused by insufficient data handling, but by suboptimal Spark configuration and parallelism.
- The slowest stage dominates overall runtime, indicating a tuning opportunity.

#### Requirement 2: Tuning Experiments Log

Experiment 1: Reduce Shuffle Partitions

Parameter Changed:

- spark.sql.shuffle.partitions (default → reduced value)

Rationale:

- Default shuffle partitions are often too high for medium-sized datasets, increasing task scheduling and shuffle overhead.

Observed Impact:

- Reduced number of tasks in shuffle stages
- Lower scheduling overhead
- Slight improvement in stage runtime (~10–15%)

Experiment 2: Increase Effective Parallelism

Parameter Changed:

- Repartitioning data on aggregation key before shuffle-heavy operations

Rationale:

- Aligning partitioning with the group-by key improves data locality and task balance.

Observed Impact:

- More even task durations
- Reduced max task runtime
- Improved executor CPU utilization

Experiment 3: Executor Resource Balancing

Parameter Changed:

- Cores per executor (balanced to avoid oversubscription)

Rationale:
- Too many cores per executor can cause contention, while too few underutilize CPU.
  
Observed Impact:

- More stable CPU usage across executors
- Reduced GC pressure
- Noticeable reduction in slowest stage duration

#### Requirement 3: Before / After Comparison

## Performance Comparison

| Metric                     | Baseline | Tuned   |
|---------------------------|----------|---------|
| Total Runtime             | ~85s     | ~52s    |
| Slowest Stage             | ~48s     | ~26s    |
| Max Task Duration         | ~41s     | ~18s    |
| Shuffle Read Concentration| High     | Reduced |
| Executor CPU Balance      | Uneven   | Balanced|
| SLA Met (<60s)            | ❌ No    | ✅ Yes  |



#### Requirement 4: SLA Tuning Summary (≈ 190 words)

The Spark job initially failed to meet the SLA due to inefficient configuration rather than insufficient compute resources. The baseline execution revealed a dominant slow stage, long-running straggler tasks, and uneven executor utilization. These issues were driven by excessive shuffle partitions, misaligned data partitioning, and unbalanced CPU usage across executors.

The configuration that successfully met the SLA combined reduced shuffle partitions, explicit repartitioning on the aggregation key, and balanced executor core allocation. Reducing shuffle partitions lowered task scheduling overhead, while repartitioning aligned data distribution with computation, minimizing shuffle cost and task imbalance. Adjusting cores per executor improved CPU efficiency and reduced garbage collection pressure, resulting in faster and more stable execution.

Together, these changes reduced total runtime from approximately 85 seconds to just over 50 seconds, bringing the job safely within the 60-second SLA. The primary trade-off introduced was a more deliberate tuning process and slightly higher memory usage per executor, which may increase cluster cost in large-scale environments. However, this cost is justified by improved SLA compliance, better resource utilization, and increased system reliability—key priorities in production Spark workloads.

## Key Takeaway
Meeting SLAs in Spark is a configuration problem guided by metrics—not guesswork.
Spark UI evidence should always drive tuning decisions.



