import streamlit as st
import os
import sys

# Ensure frontend root is in path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from utils.theme import apply_theme, render_sidebar
from utils.data_loader import load_latest_alerts, load_graph_summary

st.set_page_config(
    page_title="TxAnomaly - Offline Transaction & Network Anomaly Intelligence Platform",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

apply_theme()
render_sidebar()

# Hero Header
st.markdown("""
<div style="background: linear-gradient(135deg, #0f172a 0%, #1e1b4b 100%); padding: 2rem; border-radius: 8px; border: 1px solid #312e81; margin-bottom: 2rem;">
    <div style="font-size: 0.8rem; font-weight: 700; color: #818cf8; letter-spacing: 0.15em; text-transform: uppercase; margin-bottom: 0.5rem;">OFFLINE TRANSACTION & NETWORK ANOMALY INTELLIGENCE PLATFORM</div>
    <h1 style="font-size: 2.4rem; font-weight: 800; color: #f8fafc; margin-bottom: 0.5rem; letter-spacing: -0.02em;">TxAnomaly</h1>
    <p style="font-size: 1.1rem; color: #cbd5e1; max-width: 800px; margin-bottom: 0;">
        AI-assisted correlation, anomaly detection and link analysis for transaction and network metadata.
    </p>
</div>
""", unsafe_allow_html=True)

alerts_data = load_latest_alerts()
graph_summary = load_graph_summary()

# Top KPIs
col1, col2, col3, col4, col5, col6 = st.columns(6)

records_val = f"{alerts_data['summary']['valid_records']:,}" if alerts_data else "3,393"
ips_val = f"{graph_summary['node_counts'].get('IP', 201):,}" if graph_summary else "201"
addrs_val = f"{graph_summary['node_counts'].get('ADDRESS', 994):,}" if graph_summary else "994"
nodes_val = f"{graph_summary['num_nodes']:,}" if graph_summary else "4,587"
edges_val = f"{graph_summary['num_edges']:,}" if graph_summary else "11,166"
anomalies_val = f"{len(alerts_data['alerts']):,}" if alerts_data else "52"

with col1:
    st.markdown(f"""
    <div class="helios-card">
        <div class="helios-metric-label">Transactions</div>
        <div class="helios-metric-value">{records_val}</div>
        <div class="helios-metric-subtext">Processed Records</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="helios-card">
        <div class="helios-metric-label">IP Entities</div>
        <div class="helios-metric-value">{ips_val}</div>
        <div class="helios-metric-subtext">Network Nodes</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="helios-card">
        <div class="helios-metric-label">Addresses</div>
        <div class="helios-metric-value">{addrs_val}</div>
        <div class="helios-metric-subtext">Wallet Endpoints</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown(f"""
    <div class="helios-card">
        <div class="helios-metric-label">Graph Nodes</div>
        <div class="helios-metric-value">{nodes_val}</div>
        <div class="helios-metric-subtext">Total Topological</div>
    </div>
    """, unsafe_allow_html=True)

with col5:
    st.markdown(f"""
    <div class="helios-card">
        <div class="helios-metric-label">Graph Edges</div>
        <div class="helios-metric-value">{edges_val}</div>
        <div class="helios-metric-subtext">Directed Linkages</div>
    </div>
    """, unsafe_allow_html=True)

with col6:
    st.markdown(f"""
    <div class="helios-card" style="border-color: rgba(239, 68, 68, 0.4);">
        <div class="helios-metric-label">Anomalies</div>
        <div class="helios-metric-value" style="color: #f87171;">{anomalies_val}</div>
        <div class="helios-metric-subtext">Isolation Forest</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("### PLATFORM MODULES")
st.markdown("Select a module from the left sidebar navigation to begin analytical inspection:")

m1, m2, m3, m4 = st.columns(4)

with m1:
    st.markdown("""
    <div class="helios-card">
        <h4 style="margin-top:0; color: #38bdf8;">01 Overview</h4>
        <p style="font-size: 0.85rem; color: #94a3b8;">Analytical Command Center, overall platform metrics, and priority target summary.</p>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("""
    <div class="helios-card">
        <h4 style="margin-top:0; color: #38bdf8;">05 Entity Explorer</h4>
        <p style="font-size: 0.85rem; color: #94a3b8;">Universal investigation search for IP, Transaction ID, and Address entities.</p>
    </div>
    """, unsafe_allow_html=True)

with m2:
    st.markdown("""
    <div class="helios-card">
        <h4 style="margin-top:0; color: #38bdf8;">02 Alert Queue</h4>
        <p style="font-size: 0.85rem; color: #94a3b8;">Ranked investigator queue of anomalous entities requiring analytical review.</p>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("""
    <div class="helios-card">
        <h4 style="margin-top:0; color: #38bdf8;">06 Behavioral Clusters</h4>
        <p style="font-size: 0.85rem; color: #94a3b8;">Unsupervised population grouping using DBSCAN feature clustering.</p>
    </div>
    """, unsafe_allow_html=True)

with m3:
    st.markdown("""
    <div class="helios-card">
        <h4 style="margin-top:0; color: #38bdf8;">03 Investigation</h4>
        <p style="font-size: 0.85rem; color: #94a3b8;">Case-level evidence inspection, feature breakdown, and model interpretation.</p>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("""
    <div class="helios-card">
        <h4 style="margin-top:0; color: #38bdf8;">07 Pipeline</h4>
        <p style="font-size: 0.85rem; color: #94a3b8;">Technical architecture state, execution runtime, and stage diagnostics.</p>
    </div>
    """, unsafe_allow_html=True)

with m4:
    st.markdown("""
    <div class="helios-card">
        <h4 style="margin-top:0; color: #38bdf8;">04 Network Graph</h4>
        <p style="font-size: 0.85rem; color: #94a3b8;">Multi-hop topological link analysis and entity neighborhood visualization.</p>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("""
    <div class="helios-card">
        <h4 style="margin-top:0; color: #38bdf8;">08 Validation</h4>
        <p style="font-size: 0.85rem; color: #94a3b8;">Controlled scenario recovery metrics on planted development fixtures.</p>
    </div>
    """, unsafe_allow_html=True)
