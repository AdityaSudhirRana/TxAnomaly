import streamlit as st
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.theme import apply_theme, render_sidebar
from utils.data_loader import load_latest_alerts

st.set_page_config(page_title="Alert Queue - TxAnomaly", layout="wide")

apply_theme()
render_sidebar()

st.title("ALERT QUEUE")
st.markdown("##### Ranked entities requiring analytical review")
st.markdown("---")

alerts_data = load_latest_alerts()

if not alerts_data or "alerts" not in alerts_data:
    st.warning("No alerts data available from backend outputs.")
    st.stop()

alerts = alerts_data["alerts"]

# Filters Bar
col1, col2, col3, col4 = st.columns(4)

with col1:
    search_query = st.text_input("🔍 Search Entity IP / Alert ID", placeholder="e.g. 192.168.1.159 or A-009")
with col2:
    min_confidence = st.slider("Min Investigation Confidence", 0.0, 1.0, 0.50, 0.05)
with col3:
    all_clusters = sorted(list(set(a.get("cluster_id", -1) for a in alerts)))
    cluster_options = ["ALL"] + ["NOISE (-1)" if c == -1 else f"Group {c}" for c in all_clusters]
    selected_cluster = st.selectbox("Behavioral Group Filter", cluster_options)
with col4:
    priority_filter = st.selectbox("Priority Level", ["ALL", "CRITICAL (>0.85)", "HIGH (0.70-0.85)", "MEDIUM (<0.70)"])

# Apply Filters
filtered = []
for alert in alerts:
    # Text search
    if search_query:
        sq = search_query.strip().lower()
        if sq not in alert['entity_id'].lower() and sq not in alert['alert_id'].lower():
            continue
            
    # Confidence filter
    if alert['confidence'] < min_confidence:
        continue
        
    # Cluster filter
    if selected_cluster != "ALL":
        if selected_cluster == "NOISE (-1)" and alert['cluster_id'] != -1:
            continue
        elif selected_cluster.startswith("Group ") and alert['cluster_id'] != int(selected_cluster.replace("Group ", "")):
            continue
            
    # Priority filter
    conf = alert['confidence']
    if priority_filter == "CRITICAL (>0.85)" and conf <= 0.85:
        continue
    elif priority_filter == "HIGH (0.70-0.85)" and (conf > 0.85 or conf < 0.70):
        continue
    elif priority_filter == "MEDIUM (<0.70)" and conf >= 0.70:
        continue

    filtered.append(alert)

# Sort by confidence descending
filtered = sorted(filtered, key=lambda x: x['confidence'], reverse=True)

st.markdown(f"Displaying **{len(filtered)}** of **{len(alerts)}** total alerts in queue:")

table_data = []
for idx, alert in enumerate(filtered):
    conf = alert['confidence']
    priority = "CRITICAL" if conf >= 0.85 else "HIGH" if conf >= 0.70 else "MEDIUM"
    
    # Primary evidence extraction
    primary_reason = "N/A"
    if alert.get('reasons') and len(alert['reasons']) > 0:
        first_line = alert['reasons'][0].split('\n')[0]
        primary_reason = first_line.replace("Feature:", "").strip()
        
    group_str = "Noise / Unclustered" if alert['cluster_id'] == -1 else f"Group {alert['cluster_id']}"
    
    table_data.append({
        "Priority": priority,
        "Alert ID": alert['alert_id'],
        "Entity": alert['entity_id'],
        "Investigation Confidence": f"{conf:.4f}",
        "Anomaly Score": f"{alert['anomaly_score']:.4f}",
        "Behavioral Group": group_str,
        "Primary Evidence": primary_reason
    })

st.dataframe(
    table_data,
    use_container_width=True,
    hide_index=True
)

st.markdown("---")
st.markdown("### QUICK INVESTIGATION ACTION")

col_sel, col_btn = st.columns([3, 1])

with col_sel:
    investigate_choice = st.selectbox(
        "Select Entity from Queue to Open Detailed Case",
        options=[f"{a['alert_id']} - {a['entity_id']} (Confidence: {a['confidence']:.2f})" for a in filtered] if filtered else ["None Available"]
    )

with col_btn:
    st.markdown("<div style='height: 28px;'></div>", unsafe_allow_html=True)
    if st.button("🔎 Launch Case Investigation", use_container_width=True):
        if investigate_choice and investigate_choice != "None Available":
            sel_alert_id = investigate_choice.split(" - ")[0]
            sel_entity = investigate_choice.split(" - ")[1].split(" ")[0]
            st.session_state['selected_alert_id'] = sel_alert_id
            st.session_state['selected_entity'] = sel_entity
            st.success(f"Selected {sel_alert_id} ({sel_entity}). Please open **03 Investigation** from the sidebar.")
