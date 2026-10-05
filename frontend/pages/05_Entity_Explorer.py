import streamlit as st
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.theme import apply_theme, render_sidebar
from utils.data_loader import search_entity, parse_alert_reasons

st.set_page_config(page_title="Entity Explorer - TxAnomaly", layout="wide")

apply_theme()
render_sidebar()

st.title("UNIVERSAL ENTITY EXPLORER")
st.markdown("##### Multi-entity investigation search & cross-dataset correlation")
st.markdown("---")

# Search Box
search_input = st.text_input(
    "🔎 Search IP Address, Transaction ID (TXID), or Wallet Address",
    value="192.168.1.159",
    placeholder="e.g., 192.168.1.159, tx_00001, or 1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa_142"
)

if search_input:
    res = search_entity(search_input)
    
    if not res or not res.get("found"):
        st.error(f"❌ No matching entity found for query '{search_input.strip()}'. Check identifier spelling.")
    else:
        st.markdown(f"### IDENTITY: `{res['entity_id']}`")
        
        entity_type = res['entity_type']
        
        if entity_type == "IP":
            alert = res.get('alert')
            
            st.markdown(f"""
            <div style="background-color: #131c2e; border: 1px solid #334155; border-radius: 8px; padding: 1.2rem; margin-bottom: 1.5rem;">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.8rem;">
                    <div>
                        <span class="badge-info" style="margin-right: 8px;">ENTITY TYPE: IP ADDRESS</span>
                        <span style="font-size: 1.3rem; font-weight: 800; font-family: monospace; color: #f8fafc;">{res['entity_id']}</span>
                    </div>
                    <div>
                        {f'<span class="badge-critical">CONFIRMED ALERT {alert["alert_id"]} (RANK #{res["rank"]})</span>' if alert else '<span class="badge-ready">NO ACTIVE ALERTS</span>'}
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            c1, c2, c3, c4 = st.columns(4)
            c1.metric("Anomaly Score", f"{alert['anomaly_score']:.4f}" if alert else "0.0000")
            c2.metric("Investigation Confidence", f"{alert['confidence']:.4f}" if alert else "N/A")
            
            group_name = "Noise / Not Assigned"
            if alert and alert.get('cluster_id') != -1:
                group_name = f"Group {alert['cluster_id']}"
            c3.metric("Behavioral Group", group_name)
            c4.metric("Graph Neighborhood Size", res['neighborhood_size'])
            
            st.markdown("---")
            
            # Relevant Features & Evidence Signals
            col_left, col_right = st.columns(2)
            
            with col_left:
                st.markdown("#### RELEVANT BEHAVIORAL FEATURES")
                if alert and "features" in alert:
                    feats = alert["features"]
                    f_df = [
                        {"Metric": "Transaction Velocity", "Value": f"{feats.get('tx_velocity', 0):.2f}"},
                        {"Metric": "Destination IP Diversity", "Value": f"{feats.get('dst_ip_diversity', 0):.0f}"},
                        {"Metric": "Graph Fan-out", "Value": f"{feats.get('fan_out', 0):.0f}"},
                        {"Metric": "Address Reuse Count", "Value": f"{feats.get('address_reuse_count', 0):.0f}"},
                        {"Metric": "Total Amount Transferred", "Value": f"{feats.get('total_amount', 0):.4f}"},
                        {"Metric": "Inter-Arrival Standard Dev", "Value": f"{feats.get('inter_arrival_std', 0):.2f}"}
                    ]
                    st.dataframe(f_df, use_container_width=True, hide_index=True)
                else:
                    st.info("Standard baseline feature profile — no anomalies detected.")
                    
            with col_right:
                st.markdown("#### GRAPH NEIGHBORHOOD SUMMARY")
                st.markdown(f"**Graph Node ID:** `{res['graph_node_id']}`")
                st.markdown(f"**Direct Degree:** `{res['degree']}`")
                st.markdown(f"**Fan-out:** `{res['fan_out']}`")
                st.markdown(f"**2-Hop Neighborhood Size:** `{res['neighborhood_size']}`")
                
            st.markdown("---")
            
            # Connected Transactions & Addresses
            ct1, ct2 = st.columns(2)
            with ct1:
                st.markdown(f"#### CONNECTED TRANSACTIONS ({len(res['connected_txs'])})")
                if res['connected_txs']:
                    for tx in res['connected_txs'][:10]:
                        st.code(f"TX: {tx}")
                    if len(res['connected_txs']) > 10:
                        st.caption(f"...and {len(res['connected_txs']) - 10} more transactions.")
                else:
                    st.caption("No direct transactions mapped.")
                    
            with ct2:
                st.markdown(f"#### CONNECTED ADDRESSES ({len(res['connected_addrs'])})")
                if res['connected_addrs']:
                    for add in res['connected_addrs'][:10]:
                        st.code(f"ADDR: {add}")
                    if len(res['connected_addrs']) > 10:
                        st.caption(f"...and {len(res['connected_addrs']) - 10} more addresses.")
                else:
                    st.caption("No direct addresses mapped.")

        elif entity_type == "TX":
            st.markdown(f"""
            <div style="background-color: #131c2e; border: 1px solid #334155; border-radius: 8px; padding: 1.2rem; margin-bottom: 1.5rem;">
                <span class="badge-ready" style="margin-right: 8px;">ENTITY TYPE: TRANSACTION (TX)</span>
                <span style="font-size: 1.3rem; font-weight: 800; font-family: monospace; color: #f8fafc;">{res['entity_id']}</span>
            </div>
            """, unsafe_allow_html=True)
            
            t1, t2, t3, t4 = st.columns(4)
            t1.metric("Source IP", res['src_ip'])
            t2.metric("Destination IP", res['dst_ip'])
            t3.metric("Timestamp", res['timestamp'].split("T")[0] if "T" in res['timestamp'] else res['timestamp'])
            t4.metric("Address Outputs", len(res['addresses']))
            
            st.markdown("---")
            col_tx1, col_tx2 = st.columns(2)
            with col_tx1:
                st.markdown("#### NETWORK PORTS & ROUTING")
                st.markdown(f"**Source Port:** `{res['src_port']}`")
                st.markdown(f"**Destination Port:** `{res['dst_port']}`")
                st.markdown(f"**Graph Node ID:** `{res['graph_node_id']}`")
                
            with col_tx2:
                st.markdown("#### OUTPUT ADDRESSES & AMOUNTS")
                addr_amounts = []
                for a, amt in zip(res['addresses'], res['amounts']):
                    addr_amounts.append({"Address": a, "Amount": amt})
                st.dataframe(addr_amounts, use_container_width=True, hide_index=True)

        elif entity_type == "ADDRESS":
            st.markdown(f"""
            <div style="background-color: #131c2e; border: 1px solid #334155; border-radius: 8px; padding: 1.2rem; margin-bottom: 1.5rem;">
                <span class="badge-high" style="margin-right: 8px;">ENTITY TYPE: WALLET ADDRESS</span>
                <span style="font-size: 1.3rem; font-weight: 800; font-family: monospace; color: #f8fafc;">{res['entity_id']}</span>
            </div>
            """, unsafe_allow_html=True)
            
            a1, a2, a3 = st.columns(3)
            a1.metric("Graph Degree", res['degree'])
            a2.metric("Connected Transactions", len(res.get('connected_txs', [])))
            a3.metric("Associated IPs", len(res.get('connected_ips', [])))
            
            st.markdown("---")
            ac1, ac2 = st.columns(2)
            with ac1:
                st.markdown("#### ASSOCIATED TRANSACTIONS")
                for tx in res.get('connected_txs', [])[:10]:
                    st.code(f"TX: {tx}")
            with ac2:
                st.markdown("#### ASSOCIATED IP ENTITIES")
                for ip in res.get('connected_ips', [])[:10]:
                    st.code(f"IP: {ip}")
