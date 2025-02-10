import plotly.graph_objects as go
import pandas as pd
import networkx as nx
import numpy as np

# Load adjacency matrix from CSV
df = pd.read_csv("networks_assignment.csv", index_col=0)

# Convert to edge list
edges = df.stack().reset_index()
edges.columns = ["source", "target", "weight"]
edges = edges[edges["weight"] > 0]

# Create graph
G = nx.from_pandas_edgelist(edges, source="source", target="target", edge_attr="weight")

# Define node groups
pentagram_nodes = {'D', 'F', 'I', 'N', 'S'}
blue_nodes = pentagram_nodes
green_nodes = {'BIH', 'GEO', 'ISR', 'MNE', 'SRB', 'CHE', 'TUR', 'UKR', 'GBR', 'AUS', 'HKG', 'USA'}
yellow_nodes = {'AUT', 'BEL', 'BGR', 'HRV', 'CZE', 'EST', 'FRA', 'DEU', 'GRC', 'HUN', 'IRL', 'ITA', 'LVA', 'LUX', 'NLD', 'PRT', 'ROU', 'SVK', 'SVN', 'ESP'}

# Assign colors
node_colors = {node: ("#728FCE" if node in blue_nodes else
                      "#50C878" if node in green_nodes else
                      "#FFE135" if node in yellow_nodes else "gray") for node in G.nodes}

# Define positions manually
pos = {}

# Set pentagram positions using a star shape
radius = 2
center_x, center_y = 0, 0
angles = np.linspace(np.pi / 2, np.pi / 2 + 2 * np.pi, 6)[:-1]

pentagram_positions = {node: (center_x + radius * np.cos(a), center_y + radius * np.sin(a)) 
                       for node, a in zip(pentagram_nodes, angles)}

pos.update(pentagram_positions)

# Outer nodes
outer_nodes = set(G.nodes) - pentagram_nodes
np.random.seed(42)

min_radius = 3
max_radius = 5
node_spacing = 0.9
placed_positions = []

for node in outer_nodes:
    while True:
        angle = np.random.uniform(0, 2 * np.pi)
        radius = np.random.uniform(min_radius, max_radius)
        new_pos = (radius * np.cos(angle), radius * np.sin(angle))

        if all(np.linalg.norm(np.array(new_pos) - np.array(existing)) > node_spacing for existing in placed_positions):
            pos[node] = new_pos
            placed_positions.append(new_pos)
            break

# Extract node positions
node_x = [pos[n][0] for n in G.nodes]
node_y = [pos[n][1] for n in G.nodes]
node_colors_plot = [node_colors[n] for n in G.nodes]

# Extract edges
edge_x, edge_y, edge_hovertext = [], [], []
for edge in G.edges:
    x0, y0 = pos[edge[0]]
    x1, y1 = pos[edge[1]]
    edge_x.extend([x0, x1, None])
    edge_y.extend([y0, y1, None])
    edge_hovertext.append(f"{edge[0]} → {edge[1]}: {G[edge[0]][edge[1]]['weight']}")

# Create figure
fig = go.Figure()

# Add edges
fig.add_trace(go.Scatter(
    x=edge_x, y=edge_y,
    line=dict(width=1, color='black'),
    mode='lines',
    hovertext=edge_hovertext,
    hoverinfo="text"
))

# Edge endpoint circles
# Adjust edge-end circle positioning to touch node borders precisely
# Adjust edge-end circle positioning to touch node borders precisely
edge_end_x = []
edge_end_y = []

# Fine-tuned node marker radius for precise placement
node_marker_radius = 28 * 0.012  # Slightly reduced scaling factor

for edge in G.edges:
    x0, y0 = pos[edge[0]]
    x1, y1 = pos[edge[1]]

    # Compute edge direction
    dx, dy = x1 - x0, y1 - y0
    length = np.sqrt(dx**2 + dy**2)

    if length > 0:  # Avoid division by zero
        dx /= length
        dy /= length

        # Move circles even closer to the nodes
        edge_end_x.extend([x0 + dx * node_marker_radius, x1 - dx * node_marker_radius])
        edge_end_y.extend([y0 + dy * node_marker_radius, y1 - dy * node_marker_radius])

# Add small circular markers at edge endpoints
fig.add_trace(go.Scatter(
    x=edge_end_x, y=edge_end_y,
    mode='markers',
    marker=dict(size=6, color='black'),  # Small circles at edge endpoints
    hoverinfo='none',
    showlegend=False
))



# Add nodes
fig.add_trace(go.Scatter(
    x=node_x, y=node_y,
    mode='markers+text',
    marker=dict(size=27, color=node_colors_plot),
    text=[node if node in pentagram_nodes else "" for node in G.nodes],
    hovertext=[f"{node} (Degree: {G.degree[node]})" for node in G.nodes],
    hoverinfo="text",
    textposition="middle center",
    textfont=dict(size=12, color="white")
))

# Update layout
fig.update_layout(
    title="Network Graph with Pentagram Structure",
    showlegend=False,
    xaxis=dict(showgrid=False, zeroline=False, showticklabels=False, scaleanchor="y"),
    yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
    plot_bgcolor='white',
    font_size=12,
    width=700,
    height=700
)

fig.show()