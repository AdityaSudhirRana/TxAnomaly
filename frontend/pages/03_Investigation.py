import streamlit as st
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.theme import apply_theme, render_sidebar
from utils.data_loader import load_latest_alerts, parse_alert_reasons

st.set_page_config(page_title="Investigation Case - TxAnomaly", layout="wide")

apply_theme()
render_sidebar()

st.title("CASE INVESTIGATION WORKSPACE")
st.markdown("##### Detailed evidence inspection and diagnostic correlation")
st.markdown("---")

alerts_data = load_latest_alerts()
if not alerts_data or "alerts" not in alerts_data:
    st.warning("Alerts data unavailable.")
    st.stop()

alerts = alerts_data["alerts"]
alert_map = {a['alert_id']: a for a in alerts}
alert_options = [f"{a['alert_id']} - {a['entity_id']}" for a in alerts]

# Default selection: A-009 if available or session state
default_alert_id = st.session_state.get('selected_alert_id', 'A-009')
default_index = 0
for idx, a in enumerate(alerts):
    if a['alert_id'] == default_alert_id:
        default_index = idx
        break

c_sel, c_btn = st.columns([2, 1])

with c_sel:
    selected_option = st.selectbox(
        "Select Investigation Target",
        options=alert_options,
        index=default_index
    )

selected_alert_id = selected_option.split(" - ")[0]
alert = alert_map.get(selected_alert_id, alerts[0])

# Update session state
st.session_state['selected_alert_id'] = alert['alert_id']
st.session_state['selected_entity'] = alert['entity_id']

# INVESTIGATION TARGET HERO CARD
group_name = "Noise / Not Assigned" if alert['cluster_id'] == -1 else f"Group {alert['cluster_id']}"

st.markdown(f"""
<div style="background-color: #131c2e; border: 1px solid #334155; border-radius: 8px; padding: 1.5rem; margin-bottom: 1.5rem;">
    <div style="font-size: 0.75rem; font-weight: 700; color: #38bdf8; letter-spacing: 0.1em; text-transform: uppercase;">INVESTIGATION TARGET</div>
    <div style="font-size: 2rem; font-weight: 800; color: #f8fafc; font-family: monospace; margin-bottom: 1rem;">{alert['entity_id']}</div>
    <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 1rem; background-color: #0b0f19; padding: 1rem; border-radius: 6px; border: 1px solid #1e293b;">
        <div>
            <div class="helios-metric-label">Investigation Confidence</div>
            <div class="helios-metric-value" style="color: #ef4444;">{alert['confidence']:.2f}</div>
        </div>
        <div>
            <div class="helios-metric-label">Anomaly Score</div>
            <div class="helios-metric-value" style="color: #ef4444;">{alert['anomaly_score']:.2f}</div>
        </div>
        <div>
            <div class="helios-metric-label">Behavioral Group</div>
            <div class="helios-metric-value" style="color: #94a3b8; font-size: 1.3rem;">{group_name}</div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown("### EVIDENCE SIGNALS")
st.markdown("Structured behavioral and graph evidence flags identified by the ML engine:")

parsed_reasons = parse_alert_reasons(alert.get('reasons', []))

for item in parsed_reasons:
    st.markdown(f"""
    <div class="helios-card" style="border-left: 4px solid #38bdf8;">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.5rem;">
            <div style="font-size: 1.1rem; font-weight: 700; color: #38bdf8;">{item['feature']}</div>
            <div>
                <span style="font-size: 0.8rem; background: rgba(56, 189, 248, 0.1); color: #38bdf8; border: 1px solid rgba(56, 189, 248, 0.3); padding: 2px 8px; border-radius: 4px;">Baseline: {item['baseline']}</span>
            </div>
        </div>
        <div style="display: grid; grid-template-columns: 1fr 2fr 2fr; gap: 1rem; margin-top: 0.5rem; background: #0b0f19; padding: 0.8rem; border-radius: 4px;">
            <div>
                <div style="font-size: 0.7rem; color: #64748b; text-transform: uppercase;">Observed Value</div>
                <div style="font-size: 1.1rem; font-weight: 700; color: #f8fafc; font-family: monospace;">{item['observed']}</div>
            </div>
            <div>
                <div style="font-size: 0.7rem; color: #64748b; text-transform: uppercase;">Interpretation</div>
                <div style="font-size: 0.9rem; color: #cbd5e1;">{item['interpretation']}</div>
            </div>
            <div>
                <div style="font-size: 0.7rem; color: #64748b; text-transform: uppercase;">Contribution</div>
                <div style="font-size: 0.9rem; color: #cbd5e1;">{item['contribution']}</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# COMPLETE FEATURE MATRIX & GRAPH METRICS
col_feat, col_graph = st.columns([2, 1])

with col_feat:
    st.markdown("### COMPLETE FEATURE MATRIX (16 METRICS)")
    features = alert.get('features', {})
    
    f1, f2, f3, f4 = st.columns(4)
    f1.metric("Tx Count", f"{features.get('tx_count', 0):.0f}")
    f2.metric("Total Amount", f"{features.get('total_amount', 0):.2f}")
    f3.metric("Avg Amount", f"{features.get('avg_amount', 0):.4f}")
    f4.metric("Amount Variance", f"{features.get('amount_variance', 0):.2f}")
    
    f5, f6, f7, f8 = st.columns(4)
    f5.metric("Concentration", f"{features.get('amount_concentration', 0):.4f}")
    f6.metric("IP Diversity", f"{features.get('dst_ip_diversity', 0):.0f}")
    f7.metric("Port Diversity", f"{features.get('port_diversity', 0):.0f}")
    f8.metric("Address Reuse", f"{features.get('address_reuse_count', 0):.0f}")
    
    f9, f10, f11, f12 = st.columns(4)
    f9.metric("Addr/Tx Ratio", f"{features.get('address_to_tx_ratio', 0):.4f}")
    f10.metric("Tx Velocity", f"{features.get('tx_velocity', 0):.2f}")
    f11.metric("Inter-Arrival Avg", f"{features.get('inter_arrival_avg', 0):.2f}")
    f12.metric("Inter-Arrival Std", f"{features.get('inter_arrival_std', 0):.2f}")

with col_graph:
    st.markdown("### GRAPH NEIGHBORHOOD")
    g1, g2 = st.columns(2)
    g1.metric("Graph Degree", f"{features.get('graph_degree', 0):.0f}")
    g2.metric("Fan-Out", f"{features.get('fan_out', 0):.0f}")
    
    g3, g4 = st.columns(2)
    g3.metric("Fan-In", f"{features.get('fan_in', 0):.0f}")
    g4.metric("Neighborhood Size", f"{features.get('neighborhood_size', 0):.0f}")
    
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("🌐 Open in Network Graph Workspace", use_container_width=True):
        st.session_state['graph_entity'] = alert['entity_id']
        st.success(f"Configured graph focus to {alert['entity_id']}. Navigate to **04 Network Graph**.")
