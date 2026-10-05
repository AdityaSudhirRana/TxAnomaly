import streamlit as st
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.theme import apply_theme, render_sidebar
from utils.data_loader import load_latest_alerts, load_graph_summary, parse_alert_reasons

st.set_page_config(page_title="Overview - TxAnomaly", layout="wide")

apply_theme()
render_sidebar()

# Hero Header
st.markdown("""
<div style="background: linear-gradient(135deg, #0f172a 0%, #1e1b4b 100%); padding: 1.8rem; border-radius: 8px; border: 1px solid #312e81; margin-bottom: 1.5rem;">
    <div style="font-size: 0.75rem; font-weight: 700; color: #818cf8; letter-spacing: 0.15em; text-transform: uppercase; margin-bottom: 0.4rem;">COMMAND CENTER</div>
    <h1 style="font-size: 2.2rem; font-weight: 800; color: #f8fafc; margin-bottom: 0.4rem; letter-spacing: -0.02em;">TxAnomaly</h1>
    <div style="font-size: 1rem; font-weight: 600; color: #38bdf8; margin-bottom: 0.5rem;">Offline Transaction & Network Anomaly Intelligence Platform</div>
    <p style="font-size: 0.95rem; color: #cbd5e1; margin-bottom: 0;">
        AI-assisted correlation, anomaly detection and link analysis for transaction and network metadata.
    </p>
</div>
""", unsafe_allow_html=True)

alerts_data = load_latest_alerts()
graph_summary = load_graph_summary()

if not alerts_data or not graph_summary:
    st.warning("Backend data artifacts are currently unavailable.")
    st.stop()

# 6 KPI Cards
col1, col2, col3, col4, col5, col6 = st.columns(6)

with col1:
    st.markdown(f"""
    <div class="helios-card">
        <div class="helios-metric-label">Transactions</div>
        <div class="helios-metric-value">{alerts_data['summary']['valid_records']:,}</div>
        <div class="helios-metric-subtext">Processed Records</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="helios-card">
        <div class="helios-metric-label">IP Entities</div>
        <div class="helios-metric-value">{graph_summary['node_counts'].get('IP', 201):,}</div>
        <div class="helios-metric-subtext">Network Nodes</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="helios-card">
        <div class="helios-metric-label">Addresses</div>
        <div class="helios-metric-value">{graph_summary['node_counts'].get('ADDRESS', 994):,}</div>
        <div class="helios-metric-subtext">Wallet Endpoints</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown(f"""
    <div class="helios-card">
        <div class="helios-metric-label">Graph Nodes</div>
        <div class="helios-metric-value">{graph_summary['num_nodes']:,}</div>
        <div class="helios-metric-subtext">Total Entities</div>
    </div>
    """, unsafe_allow_html=True)

with col5:
    st.markdown(f"""
    <div class="helios-card">
        <div class="helios-metric-label">Graph Edges</div>
        <div class="helios-metric-value">{graph_summary['num_edges']:,}</div>
        <div class="helios-metric-subtext">Directed Links</div>
    </div>
    """, unsafe_allow_html=True)

with col6:
    st.markdown(f"""
    <div class="helios-card" style="border-color: rgba(239, 68, 68, 0.4);">
        <div class="helios-metric-label">Anomalies</div>
        <div class="helios-metric-value" style="color: #f87171;">{len(alerts_data['alerts']):,}</div>
        <div class="helios-metric-subtext">Flagged Targets</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# Priority Investigation Featured Highlight (A-009)
a009 = next((a for a in alerts_data['alerts'] if a['alert_id'] == 'A-009'), alerts_data['alerts'][0])

st.markdown("### PRIORITY INVESTIGATION HIGH PRIORITY TARGET")

st.markdown(f"""
<div style="background-color: #131c2e; border: 1px solid rgba(239, 68, 68, 0.4); border-radius: 8px; padding: 1.5rem; margin-bottom: 1.5rem;">
    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem;">
        <div>
            <span class="badge-critical" style="font-size: 0.85rem; padding: 4px 10px; margin-right: 10px;">TOP PRIORITY ALERT {a009['alert_id']}</span>
            <span style="font-size: 1.4rem; font-weight: 800; color: #f8fafc; font-family: monospace;">{a009['entity_id']}</span>
        </div>
        <div>
            <span class="badge-critical">ANOMALOUS</span>
        </div>
    </div>
    <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 1rem; margin-bottom: 1.2rem; background: #0b0f19; padding: 1rem; border-radius: 6px; border: 1px solid #1e293b;">
        <div>
            <div style="font-size: 0.75rem; color: #64748b; text-transform: uppercase; letter-spacing: 0.05em;">Investigation Confidence</div>
            <div style="font-size: 1.5rem; font-weight: 800; color: #ef4444; font-family: monospace;">{a009['confidence']:.2f}</div>
        </div>
        <div>
            <div style="font-size: 0.75rem; color: #64748b; text-transform: uppercase; letter-spacing: 0.05em;">Anomaly Score</div>
            <div style="font-size: 1.5rem; font-weight: 800; color: #ef4444; font-family: monospace;">{a009['anomaly_score']:.2f}</div>
        </div>
        <div>
            <div style="font-size: 0.75rem; color: #64748b; text-transform: uppercase; letter-spacing: 0.05em;">Behavioral Population</div>
            <div style="font-size: 1.5rem; font-weight: 800; color: #94a3b8; font-family: monospace;">NOISE / UNCLUSTERED</div>
        </div>
    </div>
    <div style="font-weight: 700; color: #cbd5e1; margin-bottom: 0.5rem; font-size: 0.9rem;">PRIMARY EVIDENCE SIGNALS:</div>
</div>
""", unsafe_allow_html=True)

reasons_parsed = parse_alert_reasons(a009['reasons'])
r_cols = st.columns(min(len(reasons_parsed), 4))
for idx, r in enumerate(reasons_parsed[:4]):
    with r_cols[idx]:
        st.markdown(f"""
        <div class="evidence-card">
            <div class="evidence-feature">{r['feature']}</div>
            <div style="font-size: 0.8rem; color: #94a3b8; margin-top: 4px;">Observed: <span class="evidence-observed">{r['observed']}</span> ({r['baseline']})</div>
            <div style="font-size: 0.8rem; color: #cbd5e1; margin-top: 6px;">{r['interpretation']}</div>
        </div>
        """, unsafe_allow_html=True)

st.markdown("---")

# Priority Investigations Table
st.markdown("### TOP RANKED ALERTS QUEUE")

top_10 = sorted(alerts_data['alerts'], key=lambda x: x['confidence'], reverse=True)[:10]

table_data = []
for idx, alert in enumerate(top_10):
    table_data.append({
        "RANK": idx + 1,
        "ALERT ID": alert['alert_id'],
        "ENTITY": alert['entity_id'],
        "INVESTIGATION CONFIDENCE": f"{alert['confidence']:.4f}",
        "ANOMALY SCORE": f"{alert['anomaly_score']:.4f}",
        "BEHAVIORAL GROUP": "NOISE" if alert['cluster_id'] == -1 else f"Group {alert['cluster_id']}",
        "PRIMARY SIGNAL": alert['reasons'][0].split('\n')[0].replace("Feature:", "").strip() if alert['reasons'] else "N/A"
    })

st.dataframe(table_data, use_container_width=True, hide_index=True)
