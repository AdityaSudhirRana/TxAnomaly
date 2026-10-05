\# TxAnomaly



\### Offline Transaction \& Network Anomaly Intelligence Platform



\*\*SIH26146 · Blockchain \& Cybersecurity · Investigation Intelligence\*\*



TxAnomaly is an offline investigation intelligence platform designed to correlate \*\*network-layer activity\*\* with \*\*transaction and wallet-layer metadata\*\*, reconstruct relationships as a graph, detect anomalous behavioral patterns using machine learning, and produce \*\*ranked, explainable investigative alerts\*\*.



The system is designed around the requirements of SIH26146 and operates without dependence on live blockchain feeds, external APIs, or cloud inference services.



\---



\## Problem



Investigating suspicious cryptocurrency activity can require correlating multiple layers of evidence:



\- Network observations

\- IP addresses and ports

\- Transaction identifiers

\- Wallet addresses

\- Transaction amounts

\- Temporal behavior

\- Graph relationships



Looking at these signals independently makes it difficult to identify coordinated or unusual behavior.



TxAnomaly combines these signals into a unified analytical pipeline:



```text

Network Metadata

&#x20;      +

Transaction Metadata

&#x20;      ↓

Normalization

&#x20;      ↓

Network ↔ Transaction Correlation

&#x20;      ↓

Entity / Transaction Graph

&#x20;      ↓

Behavioral Feature Engineering

&#x20;      ↓

Anomaly Detection

&#x20;      +

Behavioral Clustering

&#x20;      ↓

Evidence Generation

&#x20;      ↓

Ranked Investigation Alerts

&#x20;      ↓

Investigator Dashboard

```



\---



\# Core Capabilities



\## 1. Multi-Layer Correlation



TxAnomaly correlates network and transaction information to create a unified investigative view.



```text

IP

&#x20;│

&#x20;│ observed

&#x20;▼

Transaction

&#x20;│

&#x20;│ contains

&#x20;▼

Wallet Address

```



This allows investigators to move from an observed network entity to its associated transactions and addresses.



\---



\## 2. Graph-Based Investigation



The platform reconstructs relationships between:



\- IP addresses

\- Transactions

\- Wallet addresses



The resulting graph currently contains:



| Metric | Value |

|---|---:|

| Transactions | 3,393 |

| Unique IPs | 201 |

| Unique Addresses | 994 |

| Graph Nodes | 4,587 |

| Graph Edges | 11,166 |



Investigators can inspect localized \*\*1-hop and 2-hop neighborhoods\*\* instead of attempting to render the complete graph at once.



\---



\## 3. Machine Learning Anomaly Detection



TxAnomaly uses \*\*Isolation Forest\*\* for unsupervised anomaly detection.



The model evaluates behavioral features across multiple dimensions rather than relying on a single threshold.



\### Current model



```text

Model: Isolation Forest

Random State: 42

Validation Contamination: 0.26

```



The contamination value is exposed through the CLI and is set to `0.26` for the controlled development fixture because the fixture contains approximately 25% planted suspicious entities.



This parameter is intended to be recalibrated when processing another dataset.



\### Current validation result



```text

52 anomalous entities detected

```



The model successfully identifies the planted suspicious population while retaining some difficult cases where suspicious behavior overlaps with normal behavior.



\---



\# Behavioral Feature Engineering



TxAnomaly currently derives \*\*16 analytical features\*\*.



\### Temporal behavior



\- Transaction velocity

\- Average inter-arrival time

\- Inter-arrival-time standard deviation



Used to identify bursty or automated transaction behavior.



\### Network behavior



\- Destination IP diversity

\- Port diversity



Used to identify network sweeping, broadcasting, or unusually broad interaction patterns.



\### Transaction behavior



\- Transaction count

\- Total amount

\- Average amount

\- Amount variance

\- Amount concentration



Used to identify unusually large, concentrated, or irregular transaction behavior.



\### Address behavior



\- Address reuse count

\- Address-to-transaction ratio



Used to identify entities repeatedly operating through restricted or recurring address pools.



\### Graph behavior



\- Graph degree

\- Fan-in

\- Fan-out

\- Neighborhood size



Used to identify structurally unusual entities within the reconstructed relationship graph.



\---



\# Behavioral Clustering



TxAnomaly uses \*\*DBSCAN\*\* to identify behavioral populations.



```text

Model: DBSCAN

eps: 1.5

min\_samples: 3

Preprocessing: StandardScaler

```



Current controlled validation:



```text

Behavioral populations: 6

Unclustered/noise entities: 17

```



DBSCAN is used for \*\*behavioral population analysis\*\*, not entity resolution.



Entities with similar multidimensional behavioral profiles can be grouped together, allowing investigators to examine behavioral populations rather than isolated alerts.



\---



\# Explainable Alerts



TxAnomaly does not simply output:



```text

ANOMALOUS = TRUE

```



Each ranked alert contains structured evidence.



Example:



```text

Alert: A-009

Entity: 192.168.1.159



Investigation Confidence: 1.00

Anomaly Score: 1.00

Behavioral Group: Noise / Unclustered

```



Evidence:



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



Additional signals can include:



\- Destination IP diversity

\- Graph fan-out

\- Graph neighborhood size

\- Amount variance

\- Address reuse

\- Other derived behavioral features



The evidence is generated dynamically from the observed feature values and population statistics.



\---



\# Controlled Validation



Because the SIH problem statement specifies a \*\*synthetic dataset environment\*\* rather than providing live or seized transaction data, TxAnomaly includes a deterministic controlled development fixture.



The fixture contains deliberately planted behavioral scenarios so that the analytical pipeline can be evaluated against known ground truth.



\### Scenario recovery



| Scenario | Detection |

|---|---:|

| High Velocity | \*\*10/10 — 100%\*\* |

| High Fan-Out | \*\*10/10 — 100%\*\* |

| Address Reuse | \*\*7/10 — 70%\*\* |

| Multi-IP Sybil | \*\*8/10 — 80%\*\* |

| Amount / Graph Outlier | \*\*10/10 — 100%\*\* |



These numbers represent \*\*controlled development validation\*\*, not real-world fraud-detection accuracy.



The lower recovery of Address Reuse and Multi-IP Sybil scenarios demonstrates an important limitation of pointwise tabular anomaly detection: behaviors that individually resemble legitimate activity can be difficult to distinguish without stronger collective graph reasoning.



\---



\# Why the Controlled Fixture Matters



The development fixture is not presented as real Bitcoin data.



It exists to verify that:



1\. The ingestion pipeline works.

2\. Network and transaction information can be correlated.

3\. Graph relationships are reconstructed correctly.

4\. Features are calculated dynamically.

5\. The ML model produces dynamic predictions.

6\. Behavioral populations can be discovered.

7\. Known suspicious scenarios can be recovered.

8\. Explainable evidence corresponds to observed features.

9\. The entire system can reproduce its results offline.



The fixture is therefore a \*\*validation instrument\*\*, not a replacement for production investigative data.



\---



\# Dashboard



TxAnomaly provides an investigator-oriented Streamlit interface containing eight analytical modules.



\### 01 — Overview



Command-center view containing:



\- Dataset statistics

\- Pipeline state

\- Top ranked targets

\- Priority investigation

\- Evidence summary



\### 02 — Alert Queue



Ranked investigation queue containing:



\- Priority

\- Entity

\- Investigation confidence

\- Anomaly score

\- Behavioral group

\- Primary evidence



\### 03 — Investigation



Case-level inspection of a selected entity.



Displays:



\- Structured evidence

\- Observed feature values

\- Population baselines

\- Interpretations

\- Contribution to prioritization

\- Graph metrics

\- Behavioral information



\### 04 — Network Graph



Localized graph investigation with:



\- 1-hop analysis

\- 2-hop analysis

\- IP nodes

\- Transaction nodes

\- Address nodes

\- Relationship edges

\- Neighborhood metrics



The interface intentionally limits visualization to the selected neighborhood rather than attempting to render the entire graph.



\### 05 — Entity Explorer



Universal investigation search supporting:



```text

IP Address

Transaction ID

Wallet Address

```



Search results expose relationships and associated analytical information.



\### 06 — Behavioral Clusters



Displays discovered behavioral populations and allows investigators to inspect the characteristics of each group.



\### 07 — Pipeline



Technical architecture view showing:



```text

INGEST

&#x20;  ↓

NORMALIZE

&#x20;  ↓

CORRELATE

&#x20;  ↓

GRAPH

&#x20;  ↓

FEATURE ENGINEERING

&#x20;  ↓

ANOMALY DETECTION

&#x20;  ↓

BEHAVIORAL CLUSTERING

&#x20;  ↓

EVIDENCE GENERATION

&#x20;  ↓

RANKED ALERTS

```



\### 08 — Validation



Displays controlled scenario recovery and evaluation metrics.



\---



\# Architecture



```text

&#x20;                   ┌──────────────────────┐

&#x20;                   │   Synthetic Input    │

&#x20;                   │ Transaction + Network│

&#x20;                   │      Metadata        │

&#x20;                   └──────────┬───────────┘

&#x20;                              │

&#x20;                              ▼

&#x20;                   ┌──────────────────────┐

&#x20;                   │     Normalization    │

&#x20;                   └──────────┬───────────┘

&#x20;                              │

&#x20;                              ▼

&#x20;                   ┌──────────────────────┐

&#x20;                   │      Correlation     │

&#x20;                   │ Network ↔ Transaction│

&#x20;                   └──────────┬───────────┘

&#x20;                              │

&#x20;                              ▼

&#x20;                   ┌──────────────────────┐

&#x20;                   │     Graph Builder    │

&#x20;                   │       NetworkX       │

&#x20;                   └──────────┬───────────┘

&#x20;                              │

&#x20;                              ▼

&#x20;                   ┌──────────────────────┐

&#x20;                   │ Feature Engineering  │

&#x20;                   │      16 Features     │

&#x20;                   └──────────┬───────────┘

&#x20;                              │

&#x20;               ┌──────────────┴──────────────┐

&#x20;               ▼                             ▼

&#x20;     ┌──────────────────┐          ┌──────────────────┐

&#x20;     │ Isolation Forest │          │      DBSCAN      │

&#x20;     │ Anomaly Detection│          │Behavioral Groups │

&#x20;     └─────────┬────────┘          └─────────┬────────┘

&#x20;               │                             │

&#x20;               └──────────────┬──────────────┘

&#x20;                              ▼

&#x20;                   ┌──────────────────────┐

&#x20;                   │ Evidence Generation  │

&#x20;                   └──────────┬───────────┘

&#x20;                              │

&#x20;                              ▼

&#x20;                   ┌──────────────────────┐

&#x20;                   │ Ranked Alert Queue   │

&#x20;                   └──────────┬───────────┘

&#x20;                              │

&#x20;                              ▼

&#x20;                   ┌──────────────────────┐

&#x20;                   │  Investigator UI     │

&#x20;                   │      Streamlit       │

&#x20;                   └──────────────────────┘

```



\---



\# Technology Stack



| Component | Technology |

|---|---|

| Language | Python |

| Dashboard | Streamlit |

| Data Processing | Pandas / NumPy |

| Machine Learning | Scikit-learn |

| Anomaly Detection | Isolation Forest |

| Clustering | DBSCAN |

| Scaling | StandardScaler |

| Graph Analysis | NetworkX |

| Graph Export | GraphML |

| Visualization | Matplotlib |

| Data Format | CSV / JSON |

| Execution Model | Fully Offline |



No external AI API, cloud inference service, live blockchain API, or online visualization dependency is required by the current implementation.



\---



\# Repository Structure



```text

TxAnomaly/

│

├── backend/

│   ├── app/

│   │   ├── main.py

│   │   ├── pipeline.py

│   │   ├── features/

│   │   │   └── feature\_engineering.py

│   │   └── ml/

│   │       ├── anomaly.py

│   │       └── clustering.py

│   │

│   ├── data/

│   │   └── raw/

│   │       └── dev\_fixture.csv

│   │

│   └── outputs/

│       ├── latest\_alerts.json

│       ├── latest\_graph.graphml

│       ├── latest\_graph\_summary.json

│       ├── scenario\_results.json

│       ├── demo\_report.json

│       └── demo\_report.txt

│

├── frontend/

│   ├── app.py

│   ├── pages/

│   │   ├── 01\_Overview.py

│   │   ├── 02\_Alert\_Queue.py

│   │   ├── 03\_Investigation.py

│   │   ├── 04\_Network\_Graph.py

│   │   ├── 05\_Entity\_Explorer.py

│   │   ├── 06\_Behavioral\_Clusters.py

│   │   ├── 07\_Pipeline.py

│   │   └── 08\_Validation.py

│   │

│   └── utils/

│       ├── data\_loader.py

│       └── theme.py

│

├── generate\_fixture.py

├── smoke\_test.py

├── README.md

└── requirements.txt

```



\---



\# Running TxAnomaly



\## 1. Generate the controlled development dataset



```bash

python generate\_fixture.py

```



This generates the deterministic development fixture and corresponding ground truth.



\## 2. Run the intelligence pipeline



```bash

python backend/app/main.py --input backend/data/raw/dev\_fixture.csv --contamination 0.26

```



The pipeline generates:



```text

backend/outputs/latest\_alerts.json

backend/outputs/latest\_graph.graphml

backend/outputs/latest\_graph\_summary.json

backend/outputs/scenario\_results.json

backend/outputs/demo\_report.json

backend/outputs/demo\_report.txt

```



\## 3. Launch the dashboard



```bash

streamlit run frontend/app.py

```



The dashboard will be available locally through Streamlit.



\---



\# Reproducibility



The complete development pipeline is deterministic.



```text

Generate Fixture

&#x20;      ↓

Run Pipeline

&#x20;      ↓

Generate Graph

&#x20;      ↓

Extract Features

&#x20;      ↓

Run ML

&#x20;      ↓

Validate Scenarios

&#x20;      ↓

Generate Outputs

&#x20;      ↓

Load Dashboard

```



The current controlled fixture produces:



```text

Runtime: \~0.63 seconds

Records: 3,393

IPs: 201

TXIDs: 3,393

Addresses: 994

Graph Nodes: 4,587

Graph Edges: 11,166

Features: 16

Anomalies: 52

Behavioral Groups: 6

Noise: 17

```



\---



\# Validation \& Integrity



The current implementation has been verified for:



\- Ground-truth leakage prevention

\- Dynamic feature calculation

\- Dynamic ML predictions

\- Dynamic graph metrics

\- Dynamic evidence generation

\- Deterministic reproduction

\- Offline execution

\- JSON output validity

\- Backend/frontend contract consistency

\- Entity resolution between UI and GraphML node identifiers

\- IP / TXID / wallet search normalization

\- Bounded graph rendering



The frontend smoke test passes across all application modules:



```text

PASS: frontend/app.py

PASS: frontend/pages/01\_Overview.py

PASS: frontend/pages/02\_Alert\_Queue.py

PASS: frontend/pages/03\_Investigation.py

PASS: frontend/pages/04\_Network\_Graph.py

PASS: frontend/pages/05\_Entity\_Explorer.py

PASS: frontend/pages/06\_Behavioral\_Clusters.py

PASS: frontend/pages/07\_Pipeline.py

PASS: frontend/pages/08\_Validation.py

```



\---



\# Important Evaluation Note



TxAnomaly is currently demonstrated using a \*\*controlled synthetic development fixture\*\*.



The purpose of this fixture is to validate the analytical architecture and demonstrate recovery of known behavioral scenarios.



The reported scenario detection percentages \*\*must not be interpreted as production accuracy, criminal attribution, or real-world Bitcoin fraud-detection performance\*\*.



In a deployment using an official SIH-provided synthetic dataset or another authorized dataset, the same pipeline can ingest the new data and recompute its graph, features, anomaly scores, clusters, evidence, and ranked alerts.



\---



\# Current Limitations



\### Multi-entity Sybil behavior



Pointwise tabular anomaly detection can struggle when multiple entities individually resemble normal users but collectively form suspicious structures.



Current controlled recovery:



```text

MULTI\_IP\_SYBIL: 8/10

```



A future production enhancement could incorporate stronger graph-level methods such as community detection or graph neural network approaches.



\### Address reuse



Some address-reuse behavior overlaps with legitimate transaction patterns.



Current controlled recovery:



```text

ADDRESS\_REUSE: 7/10

```



This is intentionally retained as a limitation rather than artificially tuning the system to produce perfect validation numbers.



\### Graph visualization



The dashboard renders localized neighborhoods rather than the complete graph to maintain responsive investigation workflows.



\---



\# Future Extensions



Potential extensions include:



\- Community detection for coordinated multi-IP behavior

\- Temporal graph analysis

\- Graph neural networks

\- Adaptive contamination estimation

\- Additional behavioral features

\- Larger synthetic datasets

\- Integration with authorized investigation datasets

\- Advanced case management

\- Historical investigation tracking

\- More sophisticated graph visualization



These are future extensions and are not required for the current offline prototype.



\---



\# Design Philosophy



TxAnomaly is built around five principles:



\### 1. Correlate, don't isolate



Network and transaction observations become more useful when analyzed together.



\### 2. Detect behavior, not labels



The system looks for unusual behavioral patterns rather than requiring a predefined list of malicious entities.



\### 3. Explain every alert



An investigator should be able to understand \*\*why\*\* an entity was prioritized.



\### 4. Preserve analytical honesty



Controlled validation is clearly separated from real-world accuracy claims.



\### 5. Keep investigation human-directed



TxAnomaly prioritizes entities and surfaces evidence. It does not claim to establish criminal attribution.



\---



\# SIH26146 Alignment



TxAnomaly addresses the central requirements of the problem statement through:



| SIH Requirement | TxAnomaly Implementation |

|---|---|

| Bulk synthetic metadata ingestion | CSV ingestion pipeline |

| Network metadata analysis | IP, port and temporal features |

| Transaction metadata analysis | TXID, wallet and amount features |

| Network ↔ transaction correlation | Correlation pipeline |

| Relationship reconstruction | NetworkX graph |

| Graph-based analysis | Degree, fan-in, fan-out, neighborhood features |

| AI/ML anomaly detection | Isolation Forest |

| Behavioral clustering | DBSCAN |

| Explainable alerts | Dynamic evidence generation |

| Ranked investigations | Investigation confidence / ranking score |

| Investigator visualization | Streamlit dashboard |

| Offline operation | No external runtime dependency |



\---



\# Team



\*\*Kardashev-6\*\*



Built for \*\*Smart India Hackathon 2026 — SIH26146\*\*



\### Project



\*\*TxAnomaly\*\*



\### Category



\*\*Blockchain \& Cybersecurity\*\*



\### Focus



\*\*Offline Transaction \& Network Anomaly Intelligence\*\*



\---



\## Disclaimer



TxAnomaly is a research and hackathon prototype for analytical investigation support.



It does not establish criminal activity, identity, intent, or attribution. Anomaly scores and investigation rankings represent analytical prioritization signals and require human investigation and appropriate evidence before any real-world conclusion is made.



\---



\# TxAnomaly



> \*\*Correlate. Detect. Explain. Investigate.\*\*

