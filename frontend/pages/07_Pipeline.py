import streamlit as st
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.theme import apply_theme, render_sidebar
from utils.data_loader import load_demo_report

st.set_page_config(page_title="Pipeline Architecture - TxAnomaly", layout="wide")

apply_theme()
render_sidebar()

st.title("TECHNICAL PIPELINE ARCHITECTURE")
st.markdown("##### End-to-end analytical processing pipeline state & execution diagnostics")
st.markdown("---")

report = load_demo_report()
runtime_val = f"{report.get('runtime', 0.6289):.2f} seconds" if report else "0.63 seconds"

# Key Performance & Spec Header
p1, p2, p3, p4, p5 = st.columns(5)
with p1:
    st.metric("Execution Runtime", runtime_val)
with p2:
    st.metric("Behavioral Features", "16 Features")
with p3:
    st.metric("Anomaly Model", "Isolation Forest")
with p4:
    st.metric("Cluster Model", "DBSCAN")
with p5:
    st.metric("Execution Mode", "100% Offline")

st.markdown("---")
st.markdown("### PIPELINE ARCHITECTURE FLOW")

st.markdown("""
<div style="background-color: #0f172a; border: 1px solid #1e293b; border-radius: 8px; padding: 1.2rem; margin-bottom: 2rem;">
    <div style="display: flex; flex-wrap: wrap; justify-content: space-between; align-items: center; gap: 8px; font-family: monospace; font-size: 0.85rem; font-weight: 700;">
        <span style="background: #1e293b; padding: 8px 12px; border-radius: 4px; color: #38bdf8;">INGEST</span> →
        <span style="background: #1e293b; padding: 8px 12px; border-radius: 4px; color: #38bdf8;">NORMALIZE</span> →
        <span style="background: #1e293b; padding: 8px 12px; border-radius: 4px; color: #38bdf8;">CORRELATE</span> →
        <span style="background: #1e293b; padding: 8px 12px; border-radius: 4px; color: #38bdf8;">GRAPH</span> →
        <span style="background: #1e293b; padding: 8px 12px; border-radius: 4px; color: #38bdf8;">FEATURE ENGINEERING</span> →
        <span style="background: #1e293b; padding: 8px 12px; border-radius: 4px; color: #38bdf8;">ANOMALY DETECTION</span> →
        <span style="background: #1e293b; padding: 8px 12px; border-radius: 4px; color: #38bdf8;">BEHAVIORAL CLUSTERING</span> →
        <span style="background: #1e293b; padding: 8px 12px; border-radius: 4px; color: #38bdf8;">EVIDENCE</span> →
        <span style="background: rgba(16, 185, 129, 0.2); border: 1px solid rgba(16, 185, 129, 0.4); padding: 8px 12px; border-radius: 4px; color: #34d399;">RANKED ALERTS</span>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown("### PIPELINE STAGE DIAGNOSTICS")

stages = [
    {
        "stage": "01. INGEST",
        "name": "Data Ingestion & Invariant Verification",
        "purpose": "Load raw transaction logs, validate structural invariants, and quarantine corrupt records.",
        "input": "dev_fixture.csv (Raw Transactions & Network Metadata)",
        "output": "Canonical DataFrames (3,393 records)",
        "tech": "Pandas / Custom Parsers",
        "status": "COMPLETED"
    },
    {
        "stage": "02. NORMALIZE",
        "name": "Canonical Identifier Normalization",
        "purpose": "Sanitize and canonicalize IPv4 addresses, Transaction IDs, and Wallet addresses.",
        "input": "Canonical DataFrames",
        "output": "Normalized Identifier Matrices",
        "tech": "Python Standard Library / Re",
        "status": "COMPLETED"
    },
    {
        "stage": "03. CORRELATE",
        "name": "Cross-Record Correlation & Linkage",
        "purpose": "Correlate IP communication sessions with Bitcoin transactions and wallet endpoints.",
        "input": "Normalized Identifier Matrices",
        "output": "Directed Interaction Edge Lists",
        "tech": "Pandas Indexing",
        "status": "COMPLETED"
    },
    {
        "stage": "04. GRAPH",
        "name": "Topological Graph Construction",
        "purpose": "Build heterogenous directed multigraph representing topological relationships.",
        "input": "Edge Lists",
        "output": "latest_graph.graphml (4,587 nodes, 11,166 edges)",
        "tech": "NetworkX",
        "status": "COMPLETED"
    },
    {
        "stage": "05. FEATURE ENGINEERING",
        "name": "Behavioral & Graph Metric Engineering",
        "purpose": "Extract 16 high-dimensional behavioral, temporal, statistical, and graph-structural metrics per entity.",
        "input": "latest_graph.graphml & Transaction Data",
        "output": "Entity Feature Matrix (201 IPs × 16 Features)",
        "tech": "NetworkX / SciPy / NumPy",
        "status": "COMPLETED"
    },
    {
        "stage": "06. ANOMALY DETECTION",
        "name": "Unsupervised Isolation Forest Detection",
        "purpose": "Detect statistical outliers in high-dimensional feature space without relying on labels.",
        "input": "Entity Feature Matrix",
        "output": "Anomaly Scores & Isolation Tree Paths (52 Flagged)",
        "tech": "scikit-learn (Isolation Forest)",
        "status": "COMPLETED"
    },
    {
        "stage": "07. BEHAVIORAL CLUSTERING",
        "name": "Density-Based Population Clustering",
        "purpose": "Group entities with similar behavioral profiles into populations or isolate noise.",
        "input": "Entity Feature Matrix",
        "output": "DBSCAN Clusters (6 Groups + 17 Noise)",
        "tech": "scikit-learn (DBSCAN)",
        "status": "COMPLETED"
    },
    {
        "stage": "08. EVIDENCE SYNTHESIS",
        "name": "Evidence Correlation & Heuristic Scoring",
        "purpose": "Correlate ML scores with statistical percentile baselines to generate structured evidence.",
        "input": "Anomaly Scores, Clusters, Feature Matrix",
        "output": "Structured Evidence Objects & Baseline Ratios",
        "tech": "Custom Evidence Synthesis Engine",
        "status": "COMPLETED"
    },
    {
        "stage": "09. RANKED ALERTS",
        "name": "Prioritized Alert Queue Output",
        "purpose": "Rank entities by investigation confidence and produce JSON/GraphML outputs.",
        "input": "Structured Evidence Objects",
        "output": "latest_alerts.json & demo_report.json",
        "tech": "TxAnomaly Priority Heuristics",
        "status": "COMPLETED"
    }
]

for s in stages:
    with st.expander(f"**{s['stage']}: {s['name']}** — `{s['status']}`", expanded=False):
        c1, c2 = st.columns(2)
        with c1:
            st.markdown(f"**Purpose:** {s['purpose']}")
            st.markdown(f"**Technology:** `{s['tech']}`")
        with c2:
            st.markdown(f"**Input:** `{s['input']}`")
            st.markdown(f"**Output:** `{s['output']}`")
