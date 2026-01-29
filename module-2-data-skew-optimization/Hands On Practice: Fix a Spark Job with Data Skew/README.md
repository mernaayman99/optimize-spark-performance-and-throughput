# Hands-On Practice – Module 2
# Adaptive Query Execution & Skew Mitigation
## REFERENCE SOLUTION
### Scenario Recap

Following the initial Spark UI investigation in Module 1, DataWave Analytics discovered that the slowest stages are caused by shuffle-heavy operations and data skew.
In this module, the objective is to apply Adaptive Query Execution (AQE) and skew mitigation techniques, then verify their impact using Spark UI metrics.

The focus is on understanding how Spark adapts execution plans at runtime to improve parallelism and reduce shuffle cost.

### Dataset Used

Databricks Marketplace – Free Dataset

Catalog: databricks_simulated_retail_customer_data

Schema: v01

Table: sales_orders

This dataset naturally produces shuffle-heavy joins and aggregations, making it suitable for AQE demonstrations.

## Activity 1: Baseline Shuffle-Heavy Job (5 minutes)
#### Step 1: Execute a Join + Aggregation (No AQE Assumptions)

Spark Operation

- Join orders with customer attributes (self-join or derived dimension)
- Group by customer and promotion fields
- Aggregate counts
- Observed Spark UI Metrics
- Multiple shuffle stages
- High shuffle read/write sizes
- Uneven task durations
- Long-running straggler tasks

Finding

- Default execution plan does not adapt to data skew.
- Shuffle partitions remain static even when some partitions are much larger.

#### Step 2: Inspect Spark UI – Baseline

Spark UI → Jobs Tab

- Job duration exceeds expected runtime

Spark UI → Stages Tab

- Shuffle stages dominate execution
- One stage significantly longer than others

Spark UI → Task Details

- Clear straggler tasks processing disproportionate data volumes

#### ✅ Expected Output (Activity 1)

Identification of:

- Shuffle-heavy stages
- Task skew within shuffle stages
- Lack of runtime plan adaptation

#### 💡 Tips

- Static shuffle partitions are a red flag for skew.
- Long tail task durations usually indicate data imbalance.
- This baseline establishes the need for AQE.

## Activity 2: Adaptive Query Execution in Action (5 minutes)

#### ⚠️ Note
On Databricks (AWS-backed workspaces), AQE is enabled by default.
We validate AQE behavior through Spark UI evidence, not by toggling configs.

#### Step 1: Rerun the Same Job with AQE Active

Spark Behavior

- Same logical query
- Same dataset
- No manual repartitioning
- Observed Spark UI Metrics
- Shuffle partition count adjusted dynamically
- Reduced number of small tasks
- More balanced task durations

#### Step 2: Inspect AQE Effects in Spark UI

Spark UI → SQL Tab

- Physical plan shows AdaptiveSparkPlan
- Join strategy changes visible (e.g., SortMerge → Broadcast)
- Shuffle stages rewritten at runtime

Spark UI → Stages Tab

- Fewer shuffle partitions than baseline
- Faster completion of previously slow stages

#### Step 3: Task-Level Improvements

Observed Metrics

- Reduced variance between fastest and slowest tasks
- Fewer stragglers
- Improved executor utilization

Finding

- AQE dynamically corrected poor initial partitioning decisions.

#### ✅ Expected Output (Activity 2)

Evidence that:

- AQE modified the physical plan at runtime
- Shuffle partitions were coalesced
- Task skew was reduced

#### 💡 Tips

- Always confirm AQE via Spark UI plan changes, not assumptions.
- Look for “AdaptiveSparkPlan” as proof AQE is active.
- Reduced task imbalance is the strongest AQE success signal.

## Activity 3: Explicit Skew Mitigation Techniques (10 minutes)
#### Step 1: Apply Salting to Skewed Keys

Technique

- Add a random salt column to heavily skewed join keys
- Group by (key, salt) instead of key
- Observed Spark UI Metrics
- Shuffle load distributed across more tasks
- Previously large partitions broken into smaller ones

Finding

- Salting prevents single partitions from dominating execution.

#### Step 2: Broadcast Join Optimization

Technique

- Broadcast smaller dimension tables
- Observed Spark UI Metrics
- Shuffle stage eliminated
- Join executed locally on executors
- Job runtime reduced

Finding

- Broadcast joins are one of the most effective ways to eliminate shuffle cost.

#### ✅ Expected Output (Activity 3)

Confirmation that:

- Shuffle volume is reduced
- Join strategies changed
- Parallelism increased

#### 💡 Tips

- Broadcast joins are ideal when one side fits in memory.
- Salting should be used only for known skewed keys.
- AQE + salting provides the best results for unpredictable skew.

## Compile Your Findings
#### Requirement 1: Skew Diagnosis
Spark Job Bottleneck Analysis (3–5 Findings)

##### Finding 1: Uneven Task Durations Indicate Data Skew
Spark UI Evidence

- In the Stages tab, a small number of tasks run significantly longer than the majority.
- Maximum task duration is several times higher than the median task duration.

Explanation

- When only a few tasks dominate stage runtime, this strongly indicates data skew.
- Spark cannot complete the stage until the slowest tasks finish, even if most tasks complete quickly.

##### Finding 2: Disproportionate Shuffle Read on Few Tasks
Spark UI Evidence

- Shuffle Read Size is heavily concentrated in a small subset of tasks.
- Most tasks read minimal data, while a few tasks read very large volumes.

Explanation

- This pattern shows that certain partition keys (e.g., dominant product_id or country) receive far more records than others.
- Skewed keys cause partitions to grow unevenly, leading to shuffle-heavy straggler tasks.

##### Finding 3: Executor Spill-to-Disk Events
Spark UI Evidence

- Executors show disk spill activity during shuffle-heavy stages.
- Elevated memory usage and GC time are visible in the Executors tab.

Explanation

- Skewed partitions exceed executor memory limits, forcing Spark to spill intermediate data to disk.
- Disk I/O significantly increases task runtime and amplifies the impact of skew.

##### Finding 4: Uneven Executor Utilization
Spark UI Evidence

- Some executors are busy processing skewed tasks, while others are idle or lightly utilized.

Explanation

- Skew prevents balanced workload distribution, reducing effective cluster parallelism.
- This leads to poor resource utilization despite available compute capacity.

#### Requirement 2: Optimization Recommendations
(Linked Directly to Spark UI Evidence)
##### Recommendation 1: Apply Salting to Skewed Keys
Observed Issue

- A small number of keys dominate shuffle size and task duration.


Why This Works

- Salting artificially spreads records with dominant keys across multiple partitions.
- This reduces partition size, shortens straggler tasks, and improves parallelism.

Trade-off

- Slight increase in code complexity and downstream aggregation logic.

##### Recommendation 2: Use Broadcast Joins for Small Dimension Tables
Observed Issue

- Join stages introduce heavy shuffle and skew-related spill events.

Why This Works

- Broadcasting small tables eliminates shuffle on the join operation.
- Each executor joins locally, preventing skewed shuffle partitions.

Trade-off

- Requires confidence that the broadcasted table fits in executor memory.

##### Recommendation 3: Enable and Rely on Adaptive Query Execution (AQE)
Observed Issue

- Static partitioning does not adapt well to runtime skew patterns.

Why This Works

AQE dynamically:

- Splits skewed partitions
- Adjusts shuffle partition counts
- Changes join strategies at runtime


Trade-off

- AQE decisions occur at runtime, so behavior may vary slightly between runs.

#### Requirement 3: Summary Assessment (≈ 190 words)
The root cause of the performance degradation in this Spark job is data skew caused by dominant keys in the retail transaction dataset. Certain products and regions appear far more frequently than others, leading to uneven partition sizes after shuffle-heavy operations such as joins and aggregations. This skew manifests in the Spark UI as long-running straggler tasks, highly concentrated shuffle reads on a few tasks, executor spill-to-disk events, and uneven CPU utilization across executors.
Skew significantly impacts performance because Spark must wait for the slowest tasks to complete before finishing a stage. Even with sufficient cluster resources, skew prevents effective parallelism and causes wasted compute capacity. Disk spills further exacerbate the issue by introducing slow I/O operations during shuffle processing.
Among the available optimization strategies, salting skewed keys combined with Adaptive Query Execution is the most effective solution. Salting directly addresses dominant keys by distributing their data across multiple partitions, while AQE provides dynamic protection against unpredictable or time-varying skew patterns. When applicable, broadcast joins further reduce shuffle overhead by eliminating skew-prone join stages entirely.
Together, these optimizations restore balanced workload distribution, reduce shuffle cost, and significantly improve job runtime stability in production Spark environments.

## Key Takeaway
- Data skew is not a resource problem — it is a data distribution problem.
- Spark UI metrics provide the evidence needed to choose the right mitigation strategy rather than guessing.
