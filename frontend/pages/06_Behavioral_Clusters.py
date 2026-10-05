import streamlit as st
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.theme import apply_theme, render_sidebar
from utils.data_loader import load_latest_alerts

st.set_page_config(page_title="Behavioral Populations - TxAnomaly", layout="wide")

apply_theme()
render_sidebar()

st.title("BEHAVIORAL POPULATIONS")
st.markdown("##### Unsupervised population grouping and feature vector clustering")

# Required explanatory note
st.info("💡 **DBSCAN groups entities with similar behavioral feature profiles; clustering is not entity resolution.**")
st.markdown("---")

alerts_data = load_latest_alerts()

if not alerts_data or "alerts" not in alerts_data:
    st.warning("No behavioral clustering outputs available.")
    st.stop()

alerts = alerts_data["alerts"]

# Group entities by cluster_id
clusters = {}
for alert in alerts:
    c_id = alert.get('cluster_id', -1)
    if c_id not in clusters:
        clusters[c_id] = []
    clusters[c_id].append(alert)

# Human readable behavior definitions for presentation
CLUSTER_DESCRIPTIONS = {
    -1: {
        "name": "NOISE / UNCLUSTERED OUTLIERS",
        "behavior": "Extreme Statistical Outliers (Distinct Anomaly Signatures)",
        "color": "#ef4444"
    },
    0: {
        "name": "BEHAVIORAL GROUP 0",
        "behavior": "High Velocity Automation & Low Variance Patterns",
        "color": "#38bdf8"
    },
    1: {
        "name": "BEHAVIORAL GROUP 1",
        "behavior": "Distributed Sybil Communication Vectors",
        "color": "#38bdf8"
    },
    2: {
        "name": "BEHAVIORAL GROUP 2",
        "behavior": "Massive Topological 2-Hop Neighborhood Expansion",
        "color": "#38bdf8"
    },
    3: {
        "name": "BEHAVIORAL GROUP 3",
        "behavior": "Extreme Wallet Address Recycling & Burst Traffic",
        "color": "#38bdf8"
    },
    4: {
        "name": "BEHAVIORAL GROUP 4",
        "behavior": "Disparate IP Sweeping with High Amount Variance",
        "color": "#38bdf8"
    },
    5: {
        "name": "BEHAVIORAL GROUP 5",
        "behavior": "High Transaction Velocity & IP Sweeping Cluster",
        "color": "#38bdf8"
    }
}

st.markdown("### IDENTIFIED POPULATIONS SUMMARY")

# Display population summary cards
summary_rows = []
for c_id, members in sorted(clusters.items()):
    info = CLUSTER_DESCRIPTIONS.get(c_id, {
        "name": f"BEHAVIORAL GROUP {c_id}",
        "behavior": "Correlated Feature Vector Silhouette",
        "color": "#38bdf8"
    })
    
    avg_conf = sum(m['confidence'] for m in members) / len(members)
    avg_score = sum(m['anomaly_score'] for m in members) / len(members)
    
    summary_rows.append({
        "Group ID": "NOISE (-1)" if c_id == -1 else f"Group {c_id}",
        "Population Size": len(members),
        "Avg Confidence": f"{avg_conf:.4f}",
        "Avg Anomaly Score": f"{avg_score:.4f}",
        "Dominant Behavioral Profile": info['behavior']
    })

st.dataframe(summary_rows, use_container_width=True, hide_index=True)

st.markdown("---")

# Detailed Group Inspection
st.markdown("### POPULATION MEMBER INSPECTOR")

group_choices = ["NOISE (-1)"] + [f"Group {c}" for c in sorted(clusters.keys()) if c != -1]
selected_group = st.selectbox("Select Population to Inspect Members", group_choices)

if selected_group == "NOISE (-1)":
    inspect_id = -1
else:
    inspect_id = int(selected_group.replace("Group ", ""))

members = clusters.get(inspect_id, [])

st.markdown(f"**Members in {selected_group}:** `{len(members)}` entities")

member_table = []
for m in members:
    # Primary signal summary without raw text junk
    sig = "N/A"
    if m.get('reasons') and len(m['reasons']) > 0:
        sig = m['reasons'][0].split('\n')[0].replace("Feature:", "").strip()
        
    member_table.append({
        "Alert ID": m['alert_id'],
        "Entity IP": m['entity_id'],
        "Confidence": f"{m['confidence']:.4f}",
        "Anomaly Score": f"{m['anomaly_score']:.4f}",
        "Primary Behavioral Signal": sig,
        "Transaction Velocity": f"{m.get('features', {}).get('tx_velocity', 0):.2f}",
        "Graph Fan-out": f"{m.get('features', {}).get('fan_out', 0):.0f}"
    })

st.dataframe(member_table, use_container_width=True, hide_index=True)
