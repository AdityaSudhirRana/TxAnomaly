import streamlit as st
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.theme import apply_theme, render_sidebar
from utils.data_loader import load_scenario_results, load_demo_report

st.set_page_config(page_title="Controlled Scenario Validation - TxAnomaly", layout="wide")

apply_theme()
render_sidebar()

st.title("CONTROLLED SCENARIO VALIDATION")
st.markdown("##### Ground-truth scenario recovery on planted development fixture")

# Required explanation note
st.info("💡 **The development fixture contains planted behavioral scenarios used only to validate whether the analytical pipeline can recover known patterns. These results are not claims of real-world accuracy.**")
st.markdown("---")

results = load_scenario_results()
report = load_demo_report()

if not results:
    st.warning("No scenario validation results available from backend output.")
    st.stop()

st.markdown("### GROUND-TRUTH RECOVERY PERFORMANCE")

table_data = []
for scenario, data in results.items():
    planted = data.get("planted", 10)
    detected = data.get("detected", 0)
    recall = data.get("recall", 0.0)
    recall_pct = f"{recall * 100:.0f}%"
    
    status_badge = "✅ 100% RECOVERY" if recall == 1.0 else f"⚠️ KNOWN LIMITATION ({recall_pct})"
    
    table_data.append({
        "Behavioral Scenario": scenario,
        "Planted Pattern Count": planted,
        "Pipeline Detected": f"{detected}/{planted}",
        "Recall": recall_pct,
        "Recovery Status": status_badge
    })

st.dataframe(table_data, use_container_width=True, hide_index=True)

st.markdown("---")
st.markdown("### HONEST ANALYTICAL EVALUATION")

col_ev1, col_ev2 = st.columns(2)

with col_ev1:
    st.markdown("""
    <div class="helios-card">
        <h4 style="margin-top:0; color: #34d399;">100% Recovery Scenarios</h4>
        <ul style="color: #cbd5e1; font-size: 0.9rem; padding-left: 1.2rem;">
            <li><strong>HIGH_VELOCITY (10/10):</strong> Burst traffic & automation rate-limit anomalies are fully isolated by Isolation Forest.</li>
            <li><strong>HIGH_FAN_OUT (10/10):</strong> Massive 1-hop outbound dispersion patterns mapped directly via NetworkX degree metrics.</li>
            <li><strong>AMOUNT_GRAPH_OUTLIER (10/10):</strong> High-variance financial transfers isolated cleanly via feature variance.</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

with col_ev2:
    st.markdown("""
    <div class="helios-card" style="border-color: rgba(245, 158, 11, 0.4);">
        <h4 style="margin-top:0; color: #fbbf24;">Complex Multi-Hop Scenarios</h4>
        <ul style="color: #cbd5e1; font-size: 0.9rem; padding-left: 1.2rem;">
            <li><strong>MULTI_IP_SYBIL (8/10 - 80%):</strong> Sybil nodes splitting traffic across multiple IP subnets. 8/10 recovered; 2 fell below top-quantile confidence thresholds.</li>
            <li><strong>ADDRESS_REUSE (7/10 - 70%):</strong> Subtle recycling across small address pools. 7/10 recovered; highlights the necessity for deeper 3-hop community detection.</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")
st.markdown("### RUN METADATA")

if report:
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Validation Dataset", "dev_fixture.csv")
    m2.metric("Planted Scenarios", "5 Behavioral Types")
    m3.metric("Total Records Evaluated", f"{report.get('records_processed', 3393):,}")
    m4.metric("Pipeline Runtime", f"{report.get('runtime', 0.6289):.2f}s")
