import json
import os
import streamlit as st
import networkx as nx
import pandas as pd

BACKEND_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "backend", "outputs")
RAW_DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "backend", "data", "raw")

@st.cache_data(ttl="1h")
def load_latest_alerts():
    file_path = os.path.join(BACKEND_DIR, "latest_alerts.json")
    if not os.path.exists(file_path):
        return None
    try:
        with open(file_path, "r") as f:
            return json.load(f)
    except Exception:
        return None

@st.cache_data(ttl="1h")
def load_graph_summary():
    file_path = os.path.join(BACKEND_DIR, "latest_graph_summary.json")
    if not os.path.exists(file_path):
        return None
    try:
        with open(file_path, "r") as f:
            return json.load(f)
    except Exception:
        return None

@st.cache_resource(ttl="1h")
def load_graph():
    file_path = os.path.join(BACKEND_DIR, "latest_graph.graphml")
    if not os.path.exists(file_path):
        return None
    try:
        return nx.read_graphml(file_path)
    except Exception:
        return None

@st.cache_data(ttl="1h")
def load_scenario_results():
    file_path = os.path.join(BACKEND_DIR, "scenario_results.json")
    if not os.path.exists(file_path):
        return None
    try:
        with open(file_path, "r") as f:
            return json.load(f)
    except Exception:
        return None

@st.cache_data(ttl="1h")
def load_demo_report():
    file_path = os.path.join(BACKEND_DIR, "demo_report.json")
    if not os.path.exists(file_path):
        return None
    try:
        with open(file_path, "r") as f:
            return json.load(f)
    except Exception:
        return None

@st.cache_data(ttl="1h")
def load_fixture_df():
    file_path = os.path.join(RAW_DATA_DIR, "dev_fixture.csv")
    if not os.path.exists(file_path):
        return None
    try:
        return pd.read_csv(file_path)
    except Exception:
        return None

def get_alert_by_entity(entity_id):
    alerts_data = load_latest_alerts()
    if not alerts_data or "alerts" not in alerts_data:
        return None
    e_str = str(entity_id).strip()
    for alert in alerts_data["alerts"]:
        if str(alert.get("entity_id")).strip() == e_str:
            return alert
    return None

def resolve_graph_node(G, query):
    if G is None or not query:
        return None
    q = str(query).strip()
    
    # 1. Exact match
    if G.has_node(q):
        return q
        
    # 2. Try prefix additions
    for prefix in ["IP:", "TX:", "ADDR:"]:
        candidate = prefix + q
        if G.has_node(candidate):
            return candidate
            
    # 3. Strip prefix if user passed IP:192..., etc.
    stripped = q
    for prefix in ["IP:", "TX:", "ADDR:", "ip:", "tx:", "addr:", "IP_", "TX_", "ADDR_"]:
        if q.lower().startswith(prefix.lower()):
            stripped = q[len(prefix):]
            break
            
    if G.has_node(stripped):
        return stripped
        
    for prefix in ["IP:", "TX:", "ADDR:"]:
        candidate = prefix + stripped
        if G.has_node(candidate):
            return candidate
            
    # 4. Check original_id attribute
    for n, d in G.nodes(data=True):
        if d.get("original_id") == q or d.get("original_id") == stripped:
            return n
            
    return None

def get_graph_ip_nodes(G):
    if G is None:
        return []
    ips = set()
    for n, d in G.nodes(data=True):
        if d.get("type") == "IP" or n.startswith("IP:"):
            orig = d.get("original_id") or n.replace("IP:", "")
            ips.add(orig)
    return sorted(list(ips))

def parse_alert_reasons(reasons):
    parsed = []
    if not reasons:
        return parsed
    for r in reasons:
        lines = [line.strip() for line in r.split('\n') if line.strip()]
        item = {
            "feature": "Behavioral Anomaly",
            "observed": "N/A",
            "baseline": "90th percentile",
            "interpretation": r,
            "contribution": "Increases prioritization for anomaly score"
        }
        for l in lines:
            if l.startswith("Feature:"):
                item["feature"] = l.replace("Feature:", "").strip()
            elif l.startswith("Observed value:"):
                item["observed"] = l.replace("Observed value:", "").strip()
            elif l.startswith("Population baseline:"):
                item["baseline"] = l.replace("Population baseline:", "").strip()
            elif l.startswith("Interpretation:"):
                item["interpretation"] = l.replace("Interpretation:", "").strip()
            elif l.startswith("Contribution:"):
                item["contribution"] = l.replace("Contribution:", "").strip()
        parsed.append(item)
    return parsed

def search_entity(query):
    if not query:
        return None
    q = str(query).strip()
    
    alerts_data = load_latest_alerts()
    graph = load_graph()
    df = load_fixture_df()
    
    resolved_node = resolve_graph_node(graph, q)
    
    # 1. Search as IP
    alert = get_alert_by_entity(q)
    if alert or (resolved_node and (resolved_node.startswith("IP:") or (graph and graph.nodes[resolved_node].get("type") == "IP"))):
        entity_id = alert["entity_id"] if alert else (graph.nodes[resolved_node].get("original_id") if resolved_node else q)
        
        # Gather connected TXs and Addrs
        connected_txs = set()
        connected_addrs = set()
        if df is not None:
            sub_df = df[(df["src_ip"] == entity_id) | (df["dst_ip"] == entity_id)]
            for _, row in sub_df.iterrows():
                connected_txs.add(str(row["txid"]))
                if pd.notna(row.get("addresses")):
                    for add in str(row["addresses"]).split(";"):
                        if add.strip(): connected_addrs.add(add.strip())
                        
        degree = 0
        fan_out = 0
        neighborhood_size = 0
        if graph and resolved_node:
            degree = graph.degree(resolved_node)
            # Find 2-hop neighborhood size
            hop1 = set(graph.neighbors(resolved_node))
            hop2 = set(hop1)
            for h in hop1:
                hop2.update(graph.neighbors(h))
            neighborhood_size = len(hop2)
            
        rank = None
        if alert and alerts_data and "alerts" in alerts_data:
            # find index
            for idx, a in enumerate(alerts_data["alerts"]):
                if a["entity_id"] == entity_id:
                    rank = idx + 1
                    break

        return {
            "found": True,
            "entity_id": entity_id,
            "entity_type": "IP",
            "alert": alert,
            "rank": rank,
            "total_alerts": len(alerts_data["alerts"]) if alerts_data else 52,
            "graph_node_id": resolved_node,
            "degree": alert["features"]["graph_degree"] if alert and "graph_degree" in alert.get("features", {}) else degree,
            "fan_out": alert["features"]["fan_out"] if alert and "fan_out" in alert.get("features", {}) else degree,
            "neighborhood_size": alert["features"]["neighborhood_size"] if alert and "neighborhood_size" in alert.get("features", {}) else neighborhood_size,
            "connected_txs": sorted(list(connected_txs)),
            "connected_addrs": sorted(list(connected_addrs)),
            "features": alert.get("features", {}) if alert else {},
            "reasons": alert.get("reasons", []) if alert else []
        }
        
    # 2. Search as TXID
    if df is not None:
        tx_matches = df[df["txid"].astype(str).str.lower() == q.lower()]
        if len(tx_matches) > 0:
            row = tx_matches.iloc[0]
            tx_id = str(row["txid"])
            addrs = [a.strip() for a in str(row.get("addresses", "")).split(";") if a.strip()]
            amounts = [a.strip() for a in str(row.get("amounts", "")).split(";") if a.strip()]
            return {
                "found": True,
                "entity_id": tx_id,
                "entity_type": "TX",
                "timestamp": str(row.get("timestamp", "")),
                "src_ip": str(row.get("src_ip", "")),
                "dst_ip": str(row.get("dst_ip", "")),
                "src_port": str(row.get("src_port", "")),
                "dst_port": str(row.get("dst_port", "")),
                "addresses": addrs,
                "amounts": amounts,
                "graph_node_id": resolved_node
            }
            
    # 3. Search as Address
    if df is not None:
        # Check if address present in addresses column
        addr_matches = df[df["addresses"].astype(str).str.contains(q, case=False, na=False)]
        if len(addr_matches) > 0 or (resolved_node and ("ADDR:" in resolved_node or (graph and graph.nodes[resolved_node].get("type") == "ADDRESS"))):
            addr_id = q
            txs = set()
            ips = set()
            for _, row in addr_matches.iterrows():
                txs.add(str(row["txid"]))
                ips.add(str(row["src_ip"]))
                ips.add(str(row["dst_ip"]))
            
            degree = len(txs)
            if graph and resolved_node:
                degree = graph.degree(resolved_node)
                
            return {
                "found": True,
                "entity_id": addr_id,
                "entity_type": "ADDRESS",
                "degree": degree,
                "connected_txs": sorted(list(txs)),
                "connected_ips": sorted(list(ips)),
                "graph_node_id": resolved_node
            }

    # 4. Fallback graph node search if matched via resolve_graph_node
    if resolved_node and graph:
        n_data = graph.nodes[resolved_node]
        ntype = n_data.get("type", "UNKNOWN")
        orig = n_data.get("original_id", q)
        neighbors = list(graph.neighbors(resolved_node))
        return {
            "found": True,
            "entity_id": orig,
            "entity_type": ntype,
            "degree": len(neighbors),
            "connected_nodes": neighbors,
            "graph_node_id": resolved_node
        }
        
    return {"found": False}
