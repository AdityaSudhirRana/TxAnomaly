# TxAnomaly — Offline Transaction & Network Anomaly Intelligence Platform

**SIH26146 · Blockchain & Cybersecurity · Kardashev-6**

TxAnomaly is an **offline analytical intelligence platform** for investigating anomalous behavior across transaction and network metadata.

The system correlates network observations with transaction and wallet information, reconstructs relationships as a graph, derives behavioral features, applies unsupervised machine learning, and produces **ranked, evidence-backed investigation alerts**.

It is designed around the core investigative workflow of SIH26146:

> **Correlate → Reconstruct → Detect → Explain → Investigate**

---

## Overview

Investigative transaction data is rarely useful when examined as isolated records.

An individual IP address, transaction, wallet address, timestamp, or transfer amount may appear legitimate in isolation. Suspicious behavior often emerges only when these observations are examined **collectively across temporal, transactional, network, and graph dimensions**.

TxAnomaly addresses this by transforming raw observations into an analytical representation:

```text
Raw Metadata
     │
     ▼
Normalization
     │
     ▼
Network ↔ Transaction Correlation
     │
     ▼
Relationship Graph
     │
     ▼
Behavioral Feature Engineering
     │
     ├───────────────┐
     ▼               ▼
Anomaly Detection   Behavioral Clustering
     │               │
     └───────┬───────┘
             ▼
      Evidence Generation
             │
             ▼
      Ranked Investigation Queue
             │
             ▼
       Investigator Console
```

The system is deliberately designed so that **ML is an analytical component rather than the entire product**. The graph provides relational context, feature engineering provides behavioral representation, machine learning identifies statistical irregularity, and the evidence layer explains why an entity was prioritized.

---

## Problem Definition

SIH26146 requires an offline system capable of working with synthetic transaction and network metadata and assisting investigators in identifying suspicious behavior.

The underlying analytical problem can be reduced to four questions:

### 01 — Who?

Which entities exhibit statistically unusual behavior?

### 02 — What?

Which behavioral characteristics make the entity unusual?

### 03 — How?

How is the entity connected to transactions, addresses, and other network entities?

### 04 — Why?

What measurable evidence caused the system to prioritize the entity?

TxAnomaly is designed around answering all four questions within a single investigation workflow.

---

## Core Architecture

```text
                         ┌─────────────────────┐
                         │    Input Metadata   │
                         │                     │
                         │ IP / Port / Time    │
                         │ TXID / Address      │
                         │ Amount / Network    │
                         └──────────┬──────────┘
                                    │
                                    ▼
                         ┌─────────────────────┐
                         │    Normalization    │
                         └──────────┬──────────┘
                                    │
                                    ▼
                         ┌─────────────────────┐
                         │     Correlation     │
                         │                     │
                         │ Network ↔ TX ↔ Addr │
                         └──────────┬──────────┘
                                    │
                                    ▼
                         ┌─────────────────────┐
                         │   Graph Construction│
                         │      NetworkX       │
                         └──────────┬──────────┘
                                    │
                                    ▼
                         ┌─────────────────────┐
                         │ Feature Engineering │
                         │     16 Features     │
                         └──────────┬──────────┘
                                    │
                    ┌───────────────┴───────────────┐
                    │                               │
                    ▼                               ▼
          ┌──────────────────┐             ┌──────────────────┐
          │ Isolation Forest │             │      DBSCAN      │
          │ Anomaly Detection│             │Behavioral Groups │
          └────────┬─────────┘             └────────┬─────────┘
                   │                                │
                   └──────────────┬─────────────────┘
                                  ▼
                       ┌─────────────────────┐
                       │ Evidence Generation │
                       └──────────┬──────────┘
                                  │
                                  ▼
                       ┌─────────────────────┐
                       │ Ranked Investigation│
                       │       Alerts        │
                       └──────────┬──────────┘
                                  │
                                  ▼
                       ┌─────────────────────┐
                       │  Investigator UI    │
                       │      Streamlit      │
                       └─────────────────────┘
```

---

## Analytical Pipeline

### 1. Ingestion

The pipeline accepts structured transaction/network metadata through the local filesystem.

The development implementation operates on CSV input and produces structured JSON and GraphML analytical artifacts.

---

### 2. Normalization

Input observations are normalized into a consistent internal representation.

This allows downstream analytical stages to operate independently of the original record representation.

---

### 3. Correlation

Network-layer and transaction-layer observations are associated through their available identifiers and relationships.

Conceptually:

```text
IP
 │
 ├── observed ──► Transaction
 │                    │
 │                    └── contains ──► Wallet Address
 │
 └── interacts ──► Network Entity
```

This correlation step is fundamental to the investigation model because suspicious behavior can span multiple layers.

---

### 4. Graph Construction

TxAnomaly reconstructs relationships using **NetworkX**.

The resulting graph represents entities and their relationships rather than treating the dataset as an independent collection of rows.

The controlled development fixture currently produces:

| Graph Metric | Value |
|---|---:|
| Nodes | 4,587 |
| Edges | 11,166 |

Graph-derived characteristics are subsequently incorporated into behavioral analysis.

---

## Behavioral Feature Engineering

TxAnomaly currently derives **16 analytical features** across five behavioral dimensions.

### Temporal

- `tx_velocity`
- `inter_arrival_avg`
- `inter_arrival_std`

These characterize transaction frequency and temporal burstiness.

### Network

- `dst_ip_diversity`
- `port_diversity`

These characterize the breadth of network interaction.

### Transaction

- `tx_count`
- `total_amount`
- `avg_amount`
- `amount_variance`
- `amount_concentration`

These characterize transaction volume, monetary behavior, and distribution.

### Address

- `address_reuse_count`
- `address_to_tx_ratio`

These characterize recurring wallet/address usage patterns.

### Graph

- `graph_degree`
- `fan_in`
- `fan_out`
- `neighborhood_size`

These characterize structural position and local connectivity within the reconstructed graph.

---

## Machine Learning Layer

TxAnomaly uses two complementary unsupervised learning components.

### Isolation Forest

Isolation Forest is used to identify entities whose multidimensional behavioral representation differs substantially from the observed population.

```text
Model:
IsolationForest

random_state:
42

Validation contamination:
0.26
```

The model operates on the engineered feature space rather than relying on manually defined single-feature thresholds.

### Why Isolation Forest?

The problem does not require a conventional supervised classifier with predefined malicious/benign labels.

Instead, the controlled validation environment allows the system to evaluate whether unsupervised anomaly detection can recover intentionally planted abnormal behavioral patterns.

---

## Behavioral Clustering

DBSCAN provides a second analytical perspective.

```text
Model:
DBSCAN

eps:
1.5

min_samples:
3

Preprocessing:
StandardScaler
```

The purpose of DBSCAN is to identify **behavioral populations**.

It answers a different question from anomaly detection:

```text
Isolation Forest
        ↓
"How unusual is this entity?"

DBSCAN
        ↓
"Which entities exhibit similar behavioral profiles?"
```

The clustering layer is therefore **not entity resolution**.

---

## Evidence Generation

A numerical anomaly score alone is insufficient for an investigator.

TxAnomaly therefore converts relevant feature deviations into structured evidence.

Example:

```text
Alert: A-009
Entity: 192.168.1.159

Investigation Confidence: 1.00
Anomaly Score: 1.00
Behavioral Group: Noise / Unclustered
```

Evidence is represented as:

```text
Feature
Observed Value
Population Baseline
Interpretation
Contribution
```

Example:

```text
Feature:
Transaction velocity

Observed value:
1351.13

Population baseline:
90th percentile

Interpretation:
Unusually high transaction activity

Contribution:
Increases prioritization for bot/automation behavior
```

This design intentionally separates:

- **Anomaly score** — model-derived statistical signal
- **Investigation confidence / ranking score** — prioritization signal
- **Evidence** — interpretable feature-level explanation
- **Graph context** — relational investigation evidence

---

## Controlled Validation

Because SIH26146 specifies a synthetic-data environment rather than providing live or seized transaction data, TxAnomaly includes a **deterministic controlled development fixture**.

The fixture contains known behavioral scenarios that allow the analytical pipeline to be evaluated against ground truth.

### Current Dataset

| Metric | Value |
|---|---:|
| Records | 3,393 |
| Unique IPs | 201 |
| Unique TXIDs | 3,393 |
| Unique Addresses | 994 |
| Suspicious Entities | 50 |
| Behavioral Features | 16 |

### Scenario Recovery

| Scenario | Detection |
|---|---:|
| High Velocity | **10/10 — 100%** |
| High Fan-Out | **10/10 — 100%** |
| Address Reuse | **7/10 — 70%** |
| Multi-IP Sybil | **8/10 — 80%** |
| Amount / Graph Outlier | **10/10 — 100%** |

These values represent **controlled development validation**.

They are not presented as production accuracy, real-world fraud-detection accuracy, or evidence of criminal activity.

The imperfect recovery of Address Reuse and Multi-IP Sybil scenarios is retained intentionally. It demonstrates that the current pointwise feature representation has limitations when suspicious behavior is distributed across multiple individually normal entities.

---

## Why the Graph Matters

A transaction table can show:

```text
IP A → TX1 → Address X
IP B → TX2 → Address X
IP C → TX3 → Address X
```

The graph exposes the shared relationship:

```text
        IP A
          │
         TX1
          │
          X
         / \
       TX2 TX3
       /     \
     IP B    IP C
```

This enables investigation of **relationships and local topology**, rather than only isolated records.

Graph-derived features such as fan-out, fan-in, degree, and neighborhood size are also incorporated into the analytical feature space.

---

## Investigator Console

The Streamlit frontend is structured as an investigation workspace rather than a conventional business dashboard.

### Overview

Provides:

- Dataset state
- Pipeline state
- Top investigation targets
- Alert prioritization
- Evidence summary

### Alert Queue

Provides:

- Ranked alerts
- Investigation confidence
- Anomaly score
- Behavioral group
- Primary evidence

### Investigation

Provides:

- Entity identity
- Feature-level evidence
- Population baselines
- Interpretations
- Contribution signals
- Graph metrics

### Network Graph

Provides:

- 1-hop neighborhood analysis
- 2-hop neighborhood analysis
- IP nodes
- Transaction nodes
- Address nodes
- Relationship inspection

The interface intentionally renders localized neighborhoods rather than the complete graph.

### Entity Explorer

Supports investigation by:

```text
IP Address
Transaction ID
Wallet Address
```

### Behavioral Populations

Allows investigators to inspect DBSCAN-derived behavioral groups.

### Pipeline

Exposes the complete analytical architecture and runtime characteristics.

### Validation

Provides controlled scenario recovery and evaluation results.

---

## Technical Stack

| Layer | Technology |
|---|---|
| Language | Python |
| Data Processing | Pandas / NumPy |
| Machine Learning | Scikit-learn |
| Anomaly Detection | Isolation Forest |
| Clustering | DBSCAN |
| Feature Scaling | StandardScaler |
| Graph Analysis | NetworkX |
| Graph Format | GraphML |
| Visualization | Matplotlib |
| Interface | Streamlit |
| Data Exchange | CSV / JSON |
| Execution | Offline |

The current system does not require:

- Cloud inference
- Live blockchain APIs
- External AI APIs
- External visualization CDNs
- Internet connectivity during runtime

---

## Repository Structure

```text
TxAnomaly/
│
├── backend/
│   ├── app/
│   │   ├── main.py
│   │   ├── pipeline.py
│   │   ├── features/
│   │   │   └── feature_engineering.py
│   │   └── ml/
│   │       ├── anomaly.py
│   │       └── clustering.py
│   │
│   ├── data/
│   │   └── raw/
│   │       └── dev_fixture.csv
│   │
│   └── outputs/
│       ├── latest_alerts.json
│       ├── latest_graph.graphml
│       ├── latest_graph_summary.json
│       ├── scenario_results.json
│       ├── demo_report.json
│       └── demo_report.txt
│
├── frontend/
│   ├── app.py
│   ├── pages/
│   │   ├── 01_Overview.py
│   │   ├── 02_Alert_Queue.py
│   │   ├── 03_Investigation.py
│   │   ├── 04_Network_Graph.py
│   │   ├── 05_Entity_Explorer.py
│   │   ├── 06_Behavioral_Clusters.py
│   │   ├── 07_Pipeline.py
│   │   └── 08_Validation.py
│   │
│   └── utils/
│       ├── data_loader.py
│       └── theme.py
│
├── generate_fixture.py
├── smoke_test.py
├── requirements.txt
└── README.md
```

---

## Running the System

### 1. Generate the Development Fixture

```bash
python generate_fixture.py
```

This generates the deterministic controlled dataset and its associated ground truth.

### 2. Execute the Intelligence Pipeline

```bash
python backend/app/main.py \
  --input backend/data/raw/dev_fixture.csv \
  --contamination 0.26
```

The pipeline generates:

```text
backend/outputs/latest_alerts.json
backend/outputs/latest_graph.graphml
backend/outputs/latest_graph_summary.json
backend/outputs/scenario_results.json
backend/outputs/demo_report.json
backend/outputs/demo_report.txt
```

### 3. Launch the Investigator Console

```bash
streamlit run frontend/app.py
```

---

## Runtime Characteristics

The controlled fixture currently executes end-to-end in approximately:

```text
0.63 seconds
```

The execution includes:

```text
Ingestion
    ↓
Normalization
    ↓
Correlation
    ↓
Graph construction
    ↓
Feature extraction
    ↓
Isolation Forest
    ↓
DBSCAN
    ↓
Evidence generation
    ↓
Alert generation
    ↓
Artifact export
```

---

## Integrity & Reproducibility

The current implementation has been verified for:

- Dynamic graph construction
- Dynamic feature calculation
- Dynamic ML inference
- Dynamic evidence generation
- Ground-truth isolation from inference
- Deterministic fixture generation
- Reproducible execution
- Offline execution
- JSON output validity
- Backend/frontend artifact compatibility
- Graph entity resolution
- IP/TXID/address search normalization

The frontend smoke test passes across all application modules:

```text
PASS: frontend/app.py
PASS: frontend/pages/01_Overview.py
PASS: frontend/pages/02_Alert_Queue.py
PASS: frontend/pages/03_Investigation.py
PASS: frontend/pages/04_Network_Graph.py
PASS: frontend/pages/05_Entity_Explorer.py
PASS: frontend/pages/06_Behavioral_Clusters.py
PASS: frontend/pages/07_Pipeline.py
PASS: frontend/pages/08_Validation.py
```

---

## Controlled Validation vs. Production Data

A critical distinction in this repository is the difference between **validation data** and **investigative data**.

The included fixture is intentionally generated with known behavioral scenarios.

Its purpose is to establish that:

1. The pipeline can ingest structured observations.
2. Network and transaction information can be correlated.
3. Graph relationships are reconstructed.
4. Behavioral features are calculated.
5. ML inference operates dynamically.
6. Behavioral populations can be identified.
7. Known anomalous scenarios can be recovered.
8. Evidence corresponds to measurable observations.
9. Results are reproducible offline.

It is therefore a **development and validation instrument**, not a representation of real seized Bitcoin activity.

---

## Current Limitations

### Multi-IP Sybil Behavior

Entities participating in coordinated behavior may individually resemble normal entities.

This creates a limitation for pointwise anomaly detection.

Current controlled recovery:

```text
MULTI_IP_SYBIL
8 / 10
80%
```

A stronger graph-level community detection layer could improve detection of coordinated multi-entity behavior.

### Address Reuse

Some address reuse patterns overlap with legitimate behavior.

Current controlled recovery:

```text
ADDRESS_REUSE
7 / 10
70%
```

The system intentionally retains these limitations rather than tuning the validation fixture to produce artificially perfect results.

### Visualization Scale

The complete graph contains thousands of nodes and edges.

The investigator console therefore renders **bounded local neighborhoods** to maintain analytical readability and responsive interaction.

---

## Future Analytical Extensions

The architecture provides clear extension points for:

- Graph community detection
- Temporal graph analysis
- Graph neural networks
- Adaptive anomaly thresholds
- Additional behavioral representations
- Larger synthetic datasets
- Advanced case management
- Historical investigation tracking
- Expanded graph analytics
- Authorized external investigation datasets

These extensions are deliberately separated from the current validated prototype.

---

## SIH26146 Alignment

| Problem Requirement | TxAnomaly Implementation |
|---|---|
| Synthetic metadata processing | Controlled transaction/network fixture |
| Network-layer analysis | IP, port and temporal features |
| Transaction analysis | TXID, address and amount features |
| Network ↔ transaction correlation | Correlation pipeline |
| Relationship reconstruction | NetworkX graph |
| Graph analysis | Degree, fan-in, fan-out, neighborhood features |
| AI/ML anomaly detection | Isolation Forest |
| Behavioral clustering | DBSCAN |
| Explainable investigation | Feature-level evidence |
| Alert prioritization | Investigation ranking |
| Investigator visualization | Streamlit console |
| Offline execution | Local analytical pipeline |

---

## Design Principles

### Correlate, Don't Isolate

Independent records become more informative when analyzed as a connected system.

### Detect Behavior, Not Just Rules

The analytical engine evaluates multidimensional behavioral deviations rather than relying exclusively on manually authored thresholds.

### Explain Every Priority

An investigation target should be accompanied by measurable evidence.

### Preserve Analytical Honesty

Controlled validation is explicitly separated from claims about real-world accuracy.

### Keep the Investigator in Control

TxAnomaly prioritizes analytical leads. It does not claim to establish identity, intent, criminality, or attribution.

---

## Project Identity

**Project:** TxAnomaly  
**Problem Statement:** SIH26146  
**Domain:** Blockchain & Cybersecurity  
**Team:** Kardashev-6  
**Platform:** Offline Investigation Intelligence

---

## Disclaimer

TxAnomaly is a research and hackathon prototype intended for analytical investigation support.

An anomaly score, behavioral classification, or investigation ranking does **not** establish criminal activity, identity, intent, or attribution.

Any real-world investigative conclusion must be established through appropriate evidence, verification, and human analysis.

---

## License

This repository is developed as part of the **Smart India Hackathon 2026** project submission.

---

<div align="center">

### TxAnomaly

**Correlate. Detect. Explain. Investigate.**

*Offline Transaction & Network Anomaly Intelligence Platform*

</div>
