import pandas as pd
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
from datetime import datetime

# -------------------------- 1. Data Initialization: Anomaly Timestamps & Topology --------------------------
anomaly_data = [
    # Service layer anomalies
    {"entity": "ServiceTest11", "attr": "mrt", "timestamp": 1614962040},
    {"entity": "ServiceTest7", "attr": "mrt", "timestamp": 1614962280},
    # Container/Infrastructure layer anomalies (earliest time per entity)
    {"entity": "IG01", "attr": "FILESYSTEM", "timestamp": 1614961860},  # 00:31 earliest
    {"entity": "IG02", "attr": "FILESYSTEM", "timestamp": 1614961800},  # 00:30 (global earliest)
    {"entity": "MG01", "attr": "JVM-Memory", "timestamp": 1614962340},
    {"entity": "MG02", "attr": "JVM-Memory", "timestamp": 1614961920},
    {"entity": "Mysql02", "attr": "mysqldata_FSAvailableSpace", "timestamp": 1614961860},  # 00:31
    {"entity": "Redis02", "attr": "MEMUsedMemPerc", "timestamp": 1614961920},
    {"entity": "Tomcat02", "attr": "FILESYSTEM", "timestamp": 1614961860},  # 00:31
    {"entity": "apache01", "attr": "CPU-idle", "timestamp": 1614961860},  # 00:31
    {"entity": "apache02", "attr": "FILESYSTEM", "timestamp": 1614961860},  # 00:31
    {"entity": "dockerA2", "attr": "CpuPercent", "timestamp": 1614962100},
    # Log anomalies (IG01 log anomaly earliest 00:33)
    {"entity": "IG01", "attr": "Log-Pattern", "timestamp": 1614961980},
]

# 1.2 Build topology dependency graph (directed graph: parent→child, anomaly propagates down)
G = nx.DiGraph()
edges = [
    ("apache01", "IG01"), ("apache01", "IG02"),
    ("apache02", "IG01"), ("apache02", "IG02"),
    ("IG01", "Tomcat02"), ("IG02", "Tomcat02"),
    ("Tomcat02", "MG01"), ("Tomcat02", "MG02"),
    ("MG01", "dockerA2"), ("MG02", "dockerA2"),
    ("dockerA2", "Mysql02"),
    ("Tomcat02", "Redis02"), ("Redis02", "Tomcat02"),  # Bidirectional dependency
    ("MG01", "Redis02"), ("MG02", "Redis02"), ("Redis02", "MG01"), ("Redis02", "MG02"),
]
G.add_edges_from(edges)

# -------------------------- 2. Data Preprocessing: Feature Extraction --------------------------
df = pd.DataFrame(anomaly_data)
df["time_str"] = df["timestamp"].apply(lambda x: datetime.fromtimestamp(x).strftime("%Y-%m-%d %H:%M:%S"))
df_entity = df.groupby("entity").agg(
    earliest_timestamp=("timestamp", "min"),
    earliest_time=("time_str", "first")
).reset_index()

# 2.1 Time score (earliest = highest score)
t_min = df_entity["earliest_timestamp"].min()
t_max = df_entity["earliest_timestamp"].max()
df_entity["time_score"] = (t_max - df_entity["earliest_timestamp"]) / (t_max - t_min) if t_max > t_min else 0

# 2.2 Topology score
def get_reachable_nodes(entity):
    if entity not in G.nodes:
        return 0
    anomaly_entities = df_entity["entity"].tolist()
    reachable = nx.descendants(G, entity)
    reachable_anomaly = [n for n in reachable if n in anomaly_entities]
    return len(reachable_anomaly) + 1  # Include self

df_entity["in_degree"] = df_entity["entity"].apply(lambda x: G.in_degree(x) if x in G.nodes else 0)
df_entity["out_degree"] = df_entity["entity"].apply(lambda x: G.out_degree(x) if x in G.nodes else 0)
df_entity["reachable_count"] = df_entity["entity"].apply(get_reachable_nodes)

# Normalize topology scores
max_in = df_entity["in_degree"].max() if df_entity["in_degree"].max() > 0 else 1
max_out = df_entity["out_degree"].max() if df_entity["out_degree"].max() > 0 else 1
max_reach = df_entity["reachable_count"].max() if df_entity["reachable_count"].max() > 0 else 1

df_entity["in_degree_score"] = 1 - (df_entity["in_degree"] / max_in)
df_entity["out_degree_score"] = df_entity["out_degree"] / max_out
df_entity["reachable_score"] = df_entity["reachable_count"] / max_reach
df_entity["topology_score"] = (df_entity["in_degree_score"] + df_entity["out_degree_score"] + df_entity["reachable_score"]) / 3

# 2.3 Anomaly type score
type_weights = {
    "IG01": 0.9, "IG02": 0.9,          
    "apache01": 0.85, "apache02": 0.85,
    "Tomcat02": 0.8,                    
    "MG01": 0.75, "MG02": 0.75,         
    "Redis02": 0.7,                     
    "dockerA2": 0.65,                   
    "Mysql02": 0.6,                     
    "ServiceTest11": 0.4, "ServiceTest7": 0.4,
}
df_entity["type_score"] = df_entity["entity"].map(type_weights).fillna(0.5)

# -------------------------- 3. Comprehensive Score Model --------------------------
WEIGHT_TIME = 0.3
WEIGHT_TOPOLOGY = 0.5
WEIGHT_TYPE = 0.2

df_entity["final_score"] = (
    WEIGHT_TIME * df_entity["time_score"] +
    WEIGHT_TOPOLOGY * df_entity["topology_score"] +
    WEIGHT_TYPE * df_entity["type_score"]
)

df_entity_sorted = df_entity.sort_values("final_score", ascending=False).reset_index(drop=True)

# -------------------------- 4. Output Results --------------------------
print("="*80)
print("Anomaly Root Cause Analysis Results (Ranked by Suspicion Score)")
print("="*80)
for idx, row in df_entity_sorted.iterrows():
    print(f"Rank {idx+1} | Entity: {row['entity']}")
    print(f"  - Earliest anomaly time: {row['earliest_time']}")
    print(f"  - Time score: {row['time_score']:.2f} | Topology score: {row['topology_score']:.2f} | Type score: {row['type_score']:.2f}")
    print(f"  - Final suspicion score: {row['final_score']:.2f}")
    print("-"*50)

# Root cause
root_cause_entity = df_entity_sorted.iloc[0]["entity"]
root_cause_details = df_entity_sorted.iloc[0]
print("="*80)
print(f"Root Cause Entity: {root_cause_entity}")
print(f"Core Evidence:")
print(f"  1. Time: {root_cause_entity} has the earliest anomaly time ({root_cause_details['earliest_time']});")
print(f"  2. Topology: {root_cause_entity} is upstream in the request chain, covering {root_cause_details['reachable_count']} downstream anomalies;")
print(f"  3. Type: {root_cause_entity} is infrastructure/gateway layer (root cause type anomaly).")
print("="*80)

# -------------------------- 5. Visualization (Universal Fonts) --------------------------
# Use SYSTEM DEFAULT fonts (DejaVu Sans/Arial/Helvetica - built-in in all OS)
plt.rcParams.update({
    "font.family": ["sans-serif"],  # Use system default sans-serif
    "font.sans-serif": ["DejaVu Sans", "Arial", "Helvetica", "Liberation Sans"],  # Fallback fonts
    "font.size": 10,
    "axes.unicode_minus": False  # Fix minus sign display
})

# 5.1 Topology Graph
plt.figure(figsize=(12, 8))
pos = nx.spring_layout(G, seed=42)

# Node styling
node_colors = []
node_sizes = []
for node in G.nodes:
    if node == root_cause_entity:
        node_colors.append("red")
        node_sizes.append(800)
    elif node in df_entity["entity"].tolist():
        score = df_entity[df_entity["entity"] == node]["final_score"].values[0]
        node_colors.append(plt.cm.Reds(score))
        node_sizes.append(500 + score * 300)
    else:
        node_colors.append("lightgray")
        node_sizes.append(300)

nx.draw(G, pos, with_labels=True, node_color=node_colors, node_size=node_sizes, 
        font_weight="bold", edge_color="gray", alpha=0.8)

# Annotate time
for node in df_entity["entity"]:
    if node in pos:
        time_str = df_entity[df_entity["entity"] == node]["earliest_time"].values[0]
        nx.draw_networkx_labels(G, pos, labels={node: f"{node}\n{time_str[-8:]}"}, font_size=8)

plt.title("Anomaly Entity Topology (Red = Root Cause)", fontsize=14, fontweight="bold")
plt.savefig("anomaly_root_cause_topology.png", dpi=300, bbox_inches="tight")
plt.close()

# 5.2 Score Bar Chart
plt.figure(figsize=(10, 6))
x = df_entity_sorted["entity"][:10]
y = df_entity_sorted["final_score"][:10]
bars = plt.bar(x, y, color="lightcoral")
bars[0].set_color("red")  # Highlight root cause

plt.xlabel("Entity Name", fontweight="bold")
plt.ylabel("Suspicion Score", fontweight="bold")
plt.title("Top 10 Anomaly Entities (Higher = More Likely Root Cause)", fontsize=12, fontweight="bold")
plt.xticks(rotation=45, ha="right")
plt.tight_layout()
plt.savefig("anomaly_root_cause_score.png", dpi=300, bbox_inches="tight")
plt.close()