# Reproducible Benchmark Suite: Reliability-Controlled Conversational Spatial Information System

This directory provides the complete, transparent, and reproducible evaluation suite comparing the **Proposed Dual Control Boundaries Architecture** against two baseline configurations and extensive ablation studies across **40 standardized conversational spatial scenarios** with **3 independent replications (N = 120 trials)** under deterministic sampling ($T = 0.0$).

---

## Directory Structure

```text
benchmark/
├── run_all.sh                      # Master reproducibility bash script (executes all benchmarks)
├── dataset_40.json                 # Complete 40-scenario benchmark dataset with ground truth CSIR
├── proposed/                       # Proposed Dual Control Boundaries Architecture (Ours)
│   ├── evaluator.php               # Autonomous evaluator executing 4-layer evaluation & field comparison
│   └── results.json                # Empirical metrics (Exact CSIR 90%, Correctness 97.5%, Grounding 100%)
├── baseline_text2sql/              # Baseline 1: Direct Text-to-SQL without SIR abstraction
│   ├── prompt.txt                  # System prompt with MySQL 8.0 DDL table schema
│   ├── runner.php                  # Automated experiment runner
│   └── results.json                # Empirical evaluation metrics & raw performance logs
├── baseline_unconstrained/         # Baseline 2: Unconstrained LLM without database grounding
│   ├── prompt.txt                  # System prompt for direct zero-database conversation
│   ├── runner.php                  # Automated experiment runner
│   └── results.json                # Empirical evaluation metrics & 14 fabricated POI taxonomy
├── ablation/                       # Empirical Invariant & Policy Ablation Suite (Table 4.7)
│   ├── runner.php                  # Automated leave-one-out invariant & policy ablation runner
│   └── results.json                # Ablation matrix metrics (A1-A6 and B1-B2)
└── README.md                       # Reproducibility documentation and execution protocol
```

---

## Experimental Setup & Hyperparameters

| Parameter | Configuration | Justification |
|---|---|---|
| **Model Family** | DeepSeek-V3 (`deepseek-chat`) / OpenAI Compatible | State-of-the-art generalist LLMs with JSON-mode support |
| **Sampling Temperature ($T$)** | `0.0` (Zero Entropy) | Guarantees deterministic, reproducible token sampling |
| **Top-p Sampling** | `1.0` | Standard greedy decode under $T=0.0$ |
| **Replication Protocol** | 3 independent batch runs ($3 \times 40 = 120$ trials) | Evaluates latency stability and inference determinism |
| **Database Engine** | MySQL 8.0.x Community Server | Native `ST_Distance_Sphere` great-circle spatial computation |
| **Coordinate Storage** | `DECIMAL(10,8)` lat, `DECIMAL(11,8)` lng | Composite index `(lat, lng)`, runtime `POINT(lng, lat)` construction |

---

## Running the Reproducible Benchmarks

### 1. Master Execution Script (All-in-One)
To execute all benchmarks (Proposed Architecture, Baseline 1, Baseline 2, and Ablation Study) sequentially:

```bash
# Mode 1: Deterministic Pipeline Evaluation (Zero network variance, validates invariants & SQL logic)
bash benchmark/run_all.sh

# Mode 2: Live LLM Inference Evaluation (Direct DeepSeek API execution)
bash benchmark/run_all.sh --live
```

### 2. Independent Component Execution

```bash
# 1. Run Proposed Full Architecture Evaluator
php benchmark/proposed/evaluator.php --mock   # Deterministic verification
php benchmark/proposed/evaluator.php --live   # Live DeepSeek API inference

# Alternatively via CI4 Spark CLI:
php spark riset:evaluasi --mock
php spark riset:evaluasi --live

# 2. Run Baseline 1: Direct Text-to-SQL (MySQL 8.0 Live DB Execution)
php benchmark/baseline_text2sql/runner.php

# 3. Run Baseline 2: Unconstrained LLM (Proximity & Entity Extraction Evaluation)
php benchmark/baseline_unconstrained/runner.php

# 4. Run Ablation Study (1,080 empirical trials: A1-A6 Invariants & B1-B2 Policies)
php benchmark/ablation/runner.php

# 5. Run Automated PHPUnit Test Suite (29 unit tests, 92 assertions, 100% PASS)
vendor/bin/phpunit
```

---

## Summary of Comparative Results ($N = 40 \times 3 = 120$ Trials)

| System Configuration | Semantic Accuracy (CSIR) | Spatial Predicate Correctness | Claim Grounding Fidelity | Fabricated POIs Observed | Mean Latency (ms) |
|---|:---:|:---:|:---:|:---:|:---:|
| **Baseline 1: Direct Text-to-SQL** | 95.00% | 82.50% | 87.50% | 3 entities | 1,820.40 ms |
| **Baseline 2: Unconstrained LLM** | 22.50% | 22.50% | 45.00% | 17 entities (35.0%) | 1,145.50 ms |
| **Proposed Full Architecture (Ours)** | **92.50% (Envelope: 90.00%)** | **100.00% (Pure: 100.00%)** | **100.00% (304/304 claims)** | **0 entities (0.00%)** | **1,340.57 ms** |

*Note: Pure Spatial Predicate Correctness ($N=36$) = 100.00% (36/36), Chit-Chat Handling ($N=2$) = 100.00% (2/2), Overall Scenario Execution Compliance ($N=40$) = 100.00% (40/40).*

---

## Summary of Ablation Study Matrix (Table 4.7 in Thesis, $N = 1,080$ Executions)

| Ablation Configuration | SIR Accuracy (%) | Grounding Fidelity (%) | Out-of-Scope Handling (%) | SQL Logic Error Incidents |
|---|:---:|:---:|:---:|:---:|
| **Full System (All 6 Invariants Active)** | **100.00%** | **100.00%** | **100.00%** | **0 incidents** |
| *A1. Without Schema & Data Type Invariant* | 95.00% | 100.00% | 100.00% | 2 incidents |
| *A2. Without Spatial Domain Invariant (Padang Bounds)* | 92.50% | 100.00% | 100.00% | 3 incidents |
| *A3. Without Spatial Operator & Distance Invariant* | 90.00% | 100.00% | 100.00% | 4 incidents |
| *A4. Without Spatial Reference Coordinate Invariant* | 95.00% | 100.00% | 100.00% | 2 incidents |
| *A5. Without Operational & Price Invariant* | 97.50% | 100.00% | 100.00% | 1 incident |
| *A6. Without Ontological Scope Invariant* | 95.00% | 95.00% | 0.00% | 0 incidents |
| *B1. Without Spatial Fallback Handler* | 97.50% | 97.50% | 100.00% | 1 incident |
| *B2. Without Claim-Level Grounding Validator* | 100.00% | 85.00% | 100.00% | 0 incidents |
