import streamlit as st
import os
import sys
import networkx as nx
import matplotlib.pyplot as plt

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.theme import apply_theme, render_sidebar
from utils.data_loader import load_graph, load_latest_alerts, resolve_graph_node, get_graph_ip_nodes

st.set_page_config(page_title="Network Graph - TxAnomaly", layout="wide")

apply_theme()
render_sidebar()

st.title("NETWORK GRAPH WORKSPACE")
st.markdown("##### Topological neighborhood analysis & multi-hop graph visualization")
st.markdown("---")

graph = load_graph()
alerts_data = load_latest_alerts()

if not graph:
    st.warning("Graph dataset artifact is not available.")
    st.stop()

# Get list of valid IP nodes present in graph
graph_ips = get_graph_ip_nodes(graph)

if not graph_ips:
    st.error("No valid IP nodes found in graph artifact.")
    st.stop()

# Determine default IP (preferably 192.168.1.159)
default_ip = st.session_state.get('graph_entity', '192.168.1.159')
if default_ip not in graph_ips:
    if '192.168.1.159' in graph_ips:
        default_ip = '192.168.1.159'
    else:
        default_ip = graph_ips[0]

default_index = graph_ips.index(default_ip) if default_ip in graph_ips else 0

col_ctrl, col_main = st.columns([1, 3])

with col_ctrl:
    st.markdown("#### GRAPH CONTROLS")
    
    selected_ip = st.selectbox(
        "Selected Entity (IP)",
        options=graph_ips,
        index=default_index,
        help="Entity selector populated exclusively from IP nodes present in the graphML artifact."
    )
    
    depth = st.radio("Neighborhood Depth", [1, 2], index=0, horizontal=True)
    
    st.markdown("**Include Node Types**")
    show_ip = st.checkbox("IP Entities", value=True)
    show_tx = st.checkbox("Transactions (TX)", value=True)
    show_addr = st.checkbox("Addresses (ADDR)", value=True)
    
    st.markdown("**Include Link Types**")
    show_observed = st.checkbox("OBSERVED (IP → TX)", value=True)
    show_contains = st.checkbox("CONTAINS (TX → ADDR)", value=True)
    
    st.info("💡 **Performance Safety:** Renders bounded local neighborhood up to 2 hops.")

with col_main:
    st.markdown("#### LOCAL GRAPH NEIGHBORHOOD")
    st.caption("⚠️ **Showing selected entity neighborhood — not the complete graph.**")
    
    resolved_root = resolve_graph_node(graph, selected_ip)
    
    if not resolved_root or resolved_root not in graph:
        st.error(f"Node identifier '{selected_ip}' could not be resolved in the graph.")
    else:
        # Extract k-hop neighborhood
        nodes_in_sub = {resolved_root}
        frontier = {resolved_root}
        for _ in range(depth):
            next_frontier = set()
            for n in frontier:
                next_frontier.update(graph.neighbors(n))
            nodes_in_sub.update(next_frontier)
            frontier = next_frontier
            
        subgraph = graph.subgraph(nodes_in_sub).copy()
        
        # Apply node filters
        to_remove_nodes = []
        for n, attrs in subgraph.nodes(data=True):
            ntype = attrs.get('type', '')
            if ntype == 'IP' and not show_ip and n != resolved_root:
                to_remove_nodes.append(n)
            elif ntype == 'TX' and not show_tx:
                to_remove_nodes.append(n)
            elif ntype == 'ADDRESS' and not show_addr:
                to_remove_nodes.append(n)
        subgraph.remove_nodes_from(to_remove_nodes)
        
        # Apply edge filters
        to_remove_edges = []
        for u, v, attrs in subgraph.edges(data=True):
            rel = attrs.get('relation', attrs.get('type', ''))
            if rel == 'OBSERVED' and not show_observed:
                to_remove_edges.append((u, v))
            elif rel == 'CONTAINS' and not show_contains:
                to_remove_edges.append((u, v))
        subgraph.remove_edges_from(to_remove_edges)
        
        num_n = len(subgraph.nodes)
        num_e = len(subgraph.edges)
        
        if num_n == 0:
            st.warning("No nodes match the selected filter criteria.")
        else:
            # Render using matplotlib with dark theme
            fig, ax = plt.subplots(figsize=(10, 7), facecolor='#0b0f19')
            ax.set_facecolor('#0b0f19')
            
            # Position layout
            pos = nx.spring_layout(subgraph, k=0.3, seed=42)
            
            node_colors = []
            node_sizes = []
            labels = {}
            
            for n, attrs in subgraph.nodes(data=True):
                orig_id = attrs.get('original_id', n)
                ntype = attrs.get('type', '')
                
                if n == resolved_root:
                    node_colors.append('#ef4444') # Red for root target
                    node_sizes.append(500)
                    labels[n] = orig_id
                elif ntype == 'IP' or n.startswith('IP:'):
                    node_colors.append('#38bdf8') # Sky blue for IPs
                    node_sizes.append(250)
                    if num_n <= 30: labels[n] = orig_id
                elif ntype == 'TX' or n.startswith('TX:'):
                    node_colors.append('#34d399') # Green for TX
                    node_sizes.append(120)
                    if num_n <= 15: labels[n] = orig_id.replace("tx_", "")
                elif ntype == 'ADDRESS' or n.startswith('ADDR:'):
                    node_colors.append('#fbbf24') # Amber for Addresses
                    node_sizes.append(180)
                    if num_n <= 15: labels[n] = orig_id[:8] + "..."
                else:
                    node_colors.append('#94a3b8')
                    node_sizes.append(100)

            nx.draw_networkx_nodes(subgraph, pos, node_color=node_colors, node_size=node_sizes, alpha=0.9, ax=ax)
            nx.draw_networkx_edges(subgraph, pos, edge_color='#334155', alpha=0.5, arrows=True, arrowsize=10, ax=ax)
            
            if labels:
                nx.draw_networkx_labels(subgraph, pos, labels=labels, font_size=8, font_color='#ffffff', font_family='sans-serif', ax=ax)
                
            ax.axis('off')
            st.pyplot(fig)
            
            # Legend & Stats
            st.markdown(f"""
            <div style="background-color: #131c2e; padding: 1rem; border-radius: 6px; border: 1px solid #1e293b; margin-top: 1rem;">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <div>
                        <span style="color: #ef4444; font-weight: 700;">● Target Entity</span> &nbsp;&nbsp;
                        <span style="color: #38bdf8; font-weight: 700;">● IP Node</span> &nbsp;&nbsp;
                        <span style="color: #34d399; font-weight: 700;">● Transaction (TX)</span> &nbsp;&nbsp;
                        <span style="color: #fbbf24; font-weight: 700;">● Address (ADDR)</span>
                    </div>
                    <div style="font-family: monospace; color: #94a3b8;">
                        Sub-Graph Metrics: <strong>{num_n}</strong> Nodes | <strong>{num_e}</strong> Edges
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

            # Details Panel
            st.markdown("---")
            st.markdown("#### NEIGHBORHOOD DETAIL PANEL")
            
            d1, d2, d3 = st.columns(3)
            d1.metric("Selected Entity", selected_ip)
            d2.metric("Graph Node ID", resolved_root)
            d3.metric("Total Neighbors", graph.degree(resolved_root))
