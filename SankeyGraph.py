import pandas as pd
import plotly.graph_objects as go

# Load CSV
df = pd.read_csv('sankey_assignment.csv', index_col=0)

# Clean column and index names
df.columns = df.columns.str.strip().str.upper()
df.index = df.index.str.strip().str.upper()


sources = ['PS', 'OMP', 'CNP', 'NRP', 'NMCCC', 'PEC', 'NCDM', 'RGS']
middle_labels = ['S', 'I', 'D', 'F', 'N']  
targets = ['REG', 'ACA', 'OTH']

# Extract connections from sources to middle labels
data = []
for middle in middle_labels: 
    for source in sources:
        value = df.at[middle, source] if source in df.columns else 0
        if value > 0:
            data.append((source, middle, value))

# Extract connections from middle labels to targets, this is for the blocks in the middle
for middle in middle_labels:  
    for target in targets:
        value = df.at[middle, target] if target in df.columns else 0
        if value > 0:
            data.append((middle, target, value))

# Create label mapping 
labels = sources + middle_labels + targets
label_map = {label: i for i, label in enumerate(labels)}

# Define custom colors for bars
node_colors = {
  'PS': 'rgba(31, 119, 180, 0.8)',
    'CNP': 'rgba(44, 160, 44, 0.8)',  
    'OMP': 'rgba(255, 127, 14, 0.8)',
    'NRP': 'rgba(214, 39, 40, 0.8)',
    'NMCCC': 'rgba(148, 103, 189, 0.8)',
    'PEC': 'rgba(148, 103, 189, 0.8)',
    'NCDM': 'rgba(227, 119, 194, 0.8)',
    'RGS':'rgba(188, 189, 34, 0.8)',
    'D': 'rgba(255, 127, 14, 0.8)',  
    'N': 'rgba(214, 39, 40, 0.8)',  
    'F': 'rgba(44, 160, 44, 0.8)',  
    'I': 'rgba(128, 0, 128, 0.8)',
    'S': 'rgba(23, 190, 207, 0.8)',
    'ACA': '#98BF63',
    'REG': '#607D3B',
    'OTH': ' #466D1D'
    
}

# Assign node colors
node_color_list = [node_colors.get(label, 'lightgray') for label in labels]  # Default to lightgray

# Assign link colors
colors = [
    'rgba(31, 119, 180, 0.8)', 'rgba(255, 127, 14, 0.8)', 'rgba(44, 160, 44, 0.8)', 
    'rgba(214, 39, 40, 0.8)', 'rgba(148, 103, 189, 0.8)', 'rgba(140, 86, 75, 0.8)', 
    'rgba(227, 119, 194, 0.8)', 'rgba(188, 189, 34, 0.8)', 'rgba(23, 190, 207, 0.8)'
]

def get_color(index):
    return colors[index % len(colors)]

link_colors = [get_color(label_map[s]) for s, t, v in data]

# Create Sankey diagram
fig = go.Figure(go.Sankey(
    node=dict(
        pad=15, thickness=10, line=dict(color='black', width=0.5),
        label=labels, color=node_color_list  # Apply custom node colors
    ),
    link=dict(
        source=[label_map[s] for s, t, v in data],
        target=[label_map[t] for s, t, v in data],
        value=[v for s, t, v in data],
        color=link_colors
    )
))

fig.update_layout(title_text="Sankey Diagram", font_size=12)
fig.show()
