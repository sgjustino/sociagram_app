import streamlit as st
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from community import community_louvain  # For Louvain clustering

# Helper Functions
def load_data(uploaded_file):
    # Load data from uploaded CSV file
    data = pd.read_csv(uploaded_file, skiprows=5)
    data = data[['Group', 'Select your Number', 'Select Close Friend 1', 'How close are you to Close Friend 1?',
                 'Select Close Friend 2', 'How close are you to Close Friend 2?',
                 'Select Close Friend 3', 'How close are you to Close Friend 3?']]
    return data

def create_graph(data):
    # Initialize directed graph and add nodes and edges based on relationships
    G = nx.DiGraph()
    for _, row in data.iterrows():
        G.add_node(row['Select your Number'], label=row['Select your Number'])

    close_friends = [
        ('Select Close Friend 1', 'How close are you to Close Friend 1?'),
        ('Select Close Friend 2', 'How close are you to Close Friend 2?'),
        ('Select Close Friend 3', 'How close are you to Close Friend 3?')
    ]

    for _, row in data.iterrows():
        for friend, closeness in close_friends:
            if pd.notna(row[friend]):
                G.add_edge(row['Select your Number'], row[friend], weight=row[closeness])
    return G

def detect_clusters(G):
    # Apply Louvain clustering for community detection
    partition = community_louvain.best_partition(G.to_undirected())
    return partition

def assign_node_colors_and_styles(G, profiles):
    profile_colors = {
        "Isolates": "lightcoral",
        "Solitary": "peachpuff",
        "Star": "lightblue",
        "Interconnector": "lime"
    }
    
    node_colors = []
    node_edges = []
    edge_colors = []
    edge_widths = []

    # Set node color based on profile
    for node in G.nodes:
        if node in profiles['Isolates']:
            node_colors.append(profile_colors["Isolates"])
            node_edges.append("black")
        elif node in profiles['Solitary']:
            node_colors.append(profile_colors["Solitary"])
            node_edges.append("black")
        elif node in profiles['Star']:
            node_colors.append(profile_colors["Star"])
            node_edges.append("black")
        elif node in profiles['Interconnector']:
            node_colors.append("grey")
            node_edges.append("lime")
        else:
            node_colors.append("grey")
            node_edges.append("black")

    # Set edge colors for cliques and edge widths based on closeness
    for u, v, data in G.edges(data=True):
        if u in profiles['Cliques'] and v in profiles['Cliques']:
            edge_colors.append('#D8BFD8')  # Light purple for clique connections
            edge_widths.append(1 + data['weight'] / 2)  # Width indicates strength
        else:
            edge_colors.append('black')
            edge_widths.append(1 + data['weight'] / 2)

    return node_colors, node_edges, edge_colors, edge_widths

def draw_graph(G, profiles):
    pos = nx.circular_layout(G)
    plt.figure(figsize=(8, 6))
    node_colors, node_edges, edge_colors, edge_widths = assign_node_colors_and_styles(G, profiles)
    
    # Draw nodes with specified colors and glow for Interconnectors
    nx.draw_networkx_nodes(G, pos, node_size=900, node_color=node_colors, edgecolors=node_edges, linewidths=2)
    nx.draw_networkx_labels(G, pos, labels=nx.get_node_attributes(G, 'label'), font_size=14, font_weight='bold')
    
    # Draw edges, highlighting clique connections in light purple
    nx.draw_networkx_edges(
        G, pos, arrowstyle="->", arrowsize=15,
        edge_color=edge_colors, width=edge_widths, connectionstyle="arc3,rad=0.1"
    )
    
    # Custom legend outside the plot with larger font size and more spacing
    custom_legend = [
        Line2D([0], [0], marker='o', color='w', label='Isolates (Red)', markersize=12, markerfacecolor='lightcoral'),
        Line2D([0], [0], marker='o', color='w', label='Solitary (Orange)', markersize=12, markerfacecolor='peachpuff'),
        Line2D([0], [0], marker='o', color='w', label='Star (Blue)', markersize=12, markerfacecolor='lightblue'),
        Line2D([0], [0], marker='o', color='w', label='Interconnector (Green Glow)', markersize=12, markerfacecolor='grey', markeredgecolor='lime'),
        Line2D([0], [0], color='#D8BFD8', lw=2.5, label='Clique Connections (Purple)')
    ]
    plt.legend(handles=custom_legend, loc='upper center', bbox_to_anchor=(0.5, 1.25), fontsize='large', ncol=2, title="Relationship Profiles", title_fontsize='large')
    
    st.pyplot(plt)

def analyze_profiles(G):
    # Cluster detection for Interconnectors and Cliques
    partition = detect_clusters(G)
    profiles = {
        "Isolates": [],
        "Solitary": [],
        "Star": [],
        "Cliques": [],
        "Interconnector": []
    }

    # Define profiles
    for node in G.nodes:
        in_degree = G.in_degree(node)
        out_degree = G.out_degree(node)
        neighbors = list(G.neighbors(node))

        if in_degree == 0 and out_degree == 0:
            profiles["Isolates"].append(node)
        elif in_degree > 0 and out_degree == 0:
            profiles["Solitary"].append(node)
        elif in_degree >= 4:
            profiles["Star"].append(node)
        
        # Identify Cliques based on mutual connections within the same community and size >= 3
        clique_neighbors = [neighbor for neighbor in neighbors if G.has_edge(neighbor, node) and partition[neighbor] == partition[node]]
        if len(clique_neighbors) >= 2:
            profiles["Cliques"].append(node)
        
        # Interconnector: connects across at least 3 communities
        if len(set(partition[neighbor] for neighbor in neighbors)) >= 3:
            profiles["Interconnector"].append(node)

    return profiles

def display_recommendations(profiles):
    recommendations = {
        "Isolates": "With no connections, isolates may feel disconnected. Support them with structured group activities.",
        "Solitary": "Solitaries have incoming but no outgoing connections. Encourage them to actively participate with peers.",
        "Star": "Stars have high incoming connections and influence. Leverage their popularity to foster inclusivity.",
        "Cliques": "Cliques have mutual connections and can form closed circles. Encourage activities that integrate them with others.",
        "Interconnector": "Interconnectors bridge groups and aid in social cohesion. Engage them as peer leaders and in conflict resolution."
    }
    
    profile_colors = {
        "Isolates": "lightcoral",
        "Solitary": "peachpuff",
        "Star": "lightblue",
        "Interconnector": "palegreen",
        "Cliques": "#D8BFD8"
    }
    
    # Style recommendations with embedded CSS
    st.markdown("""
    <style>
        .profile-box {
            padding: 3px 10px 3px 10px;
            border-radius: 8px;
            margin-bottom: 8px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        }
        .profile-title {
            font-size: 16px;
            font-weight: bold;
            color: #333;
            margin-bottom: 1px;
        }
        .profile-nodes {
            font-size: 16px;
            color: #555;
            margin-bottom: 1px;
        }
        .profile-description {
            font-size: 14px;
            color: #333;
            line-height: 1.5;
            margin-bottom: 1px;
        }
    </style>
    """, unsafe_allow_html=True)
    
    # Display each profile with background color and recommendations
    for profile, description in recommendations.items():
        nodes = profiles[profile]
        node_list = ', '.join(str(node) for node in nodes) if nodes else 'None'
        
        st.markdown(f"""
        <div class="profile-box" style="background-color: {profile_colors.get(profile, 'lightgrey')};">
            <p class="profile-title">{profile}</p>
            <p class="profile-nodes"><strong>Members:</strong> {node_list}</p>
            <p class="profile-description">{description}</p>
        </div>
        """, unsafe_allow_html=True)


def display_group_metrics(connectedness, reciprocity, reachability, speed_of_communication):
    st.subheader("Group Cohesion Metrics")
    
    metrics_html = f"""
    <style>
        .metric-box {{
            background-color: #f9f9f9;
            padding: 3px 10px 3px 10px;
            border-radius: 8px;
            margin-bottom: 8px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
            position: relative;
            overflow: hidden;
        }}
        .metric-fill {{
            position: absolute;
            top: 0;
            left: 0;
            height: 100%;
            background-color: #598585;
            opacity: 0.2;
        }}
        .metric-title {{
            font-size: 16px;
            font-weight: bold;
            color: #333;
            margin-bottom: 1px;
            position: relative;
            z-index: 1;
        }}
        .metric-value {{
            font-size: 16px;
            font-weight: bold;
            color: #1f77b4;
            position: relative;
            z-index: 1;
            margin-bottom: 1px;
        }}
        .metric-description {{
            font-size: 14px;
            color: #555;
            line-height: 1.5;
            position: relative;
            z-index: 1;
            margin-bottom: 1px;
        }}
    </style>

    <div class="metric-box">
        <div class="metric-fill" style="width: {connectedness:.2f}%;"></div>
        <div class="metric-title">Connectedness</div>
        <div class="metric-value">{connectedness:.2f}%</div>
        <p class="metric-description">
            Connectedness measures the % of actual friendships relative to the maximum possible connections.
        </p>
    </div>

    <div class="metric-box">
        <div class="metric-fill" style="width: {reciprocity:.2f}%;"></div>
        <div class="metric-title">Reciprocity</div>
        <div class="metric-value">{reciprocity:.2f}%</div>
        <p class="metric-description">
            Reciprocity reflects the % of friendships that are mutual, showing relationship balance.
        </p>
    </div>

    <div class="metric-box">
        <div class="metric-fill" style="width: {reachability:.2f}%;"></div>
        <div class="metric-title">Reachability</div>
        <div class="metric-value">{reachability:.2f}%</div>
        <p class="metric-description">
            Reachability shows the % of group members who can connect directly/indirectly within the largest connected subset.
        </p>
    </div>

    <div class="metric-box">
        <div class="metric-fill" style="width: {speed_of_communication:.2f}%;"></div>
        <div class="metric-title">Speed of Communication</div>
        <div class="metric-value">{speed_of_communication:.2f}%</div>
        <p class="metric-description">
            Speed of Communication indicates how quickly information or influence can spread from the most connected person.
        </p>
    </div>
    """
    
    st.markdown(metrics_html, unsafe_allow_html=True)


def calculate_group_metrics(G):
    num_nodes = len(G.nodes)
    max_possible_connections = 3 * num_nodes

    actual_connections = G.number_of_edges()
    connectedness = (actual_connections / max_possible_connections) * 100
    
    mutual_edges = sum(1 for u, v in G.edges() if G.has_edge(v, u))
    max_possible_mutual_connections = min(actual_connections, max_possible_connections // 2)
    reciprocity = (mutual_edges / max_possible_mutual_connections) * 100 if max_possible_mutual_connections > 0 else 0

    largest_cc = max(nx.weakly_connected_components(G), key=len)
    reachability = (len(largest_cc) / num_nodes) * 100

    G_sub = G.subgraph(largest_cc).copy()
    most_connected_node = max(G_sub.degree, key=lambda x: x[1])[0]
    radius = 3
    reachable_within_3_steps = nx.single_source_shortest_path_length(G_sub, most_connected_node, cutoff=radius)
    speed_of_communication = ((len(reachable_within_3_steps) - 1) / num_nodes) * 100

    display_group_metrics(connectedness, reciprocity, reachability, speed_of_communication)

# Streamlit UI Structure
st.title("Sociogram Analysis")

# Custom CSS for boxed and scrollable tabs
st.markdown("""
<style>
    /* Overall app background */
    .stApp {
        background-color: #f0f4f8;
    }

    .stTabs [data-baseweb="tab-list"] {
        display: flex;
        overflow-x: auto;
        flex-wrap: nowrap;
        padding-bottom: 5px;
        gap: 2px;
        scrollbar-width: thin;
        background-color: #ffffff;
        border-bottom: 2px solid #e0e6ed;
    }

    .stTabs [data-baseweb="tab-list"]::-webkit-scrollbar {
        height: 8px;
    }
    .stTabs [data-baseweb="tab-list"]::-webkit-scrollbar-thumb {
        background-color: #c0c9d6;
        border-radius: 4px;
    }

    .stTabs [data-baseweb="tab"] {
        height: 40px;
        white-space: nowrap;
        background-color: #e8eef5;  /* Slightly darker than very light blue-grey */
        color: #4a5568;
        border-radius: 4px 4px 0px 0px;
        padding: 8px 16px;
        font-weight: 600;
        font-size: 14px;
        text-align: center;
        min-width: 80px;
        transition: background-color 0.3s ease, color 0.3s ease;
        border: none;
    }

    .stTabs [data-baseweb="tab"]:hover {
        background-color: #d1dce8;
        color: #2b6cb0;
    }

    .stTabs [aria-selected="true"] {
        background-color: #b8c9db;  /* Darker than tab background */
        color: #1a4971;
    }

    /* Style for the content area */
    .stTabs [data-baseweb="tab-content"] {
        background-color: #ffffff;
        border-radius: 0 0 4px 4px;
        border: 1px solid #e0e6ed;
        border-top: none;
        padding: 20px;
    }
</style>
""", unsafe_allow_html=True)


# File upload and processing
uploaded_file = st.file_uploader("Upload your data file (CSV format)", type=["csv"])
if uploaded_file:
    data = load_data(uploaded_file)
    unique_groups = data['Group'].unique()

    # Create scrollable and styled tabs with boxed appearance
    group_tabs = st.tabs([f"{group}" for group in unique_groups])

    for idx, group in enumerate(unique_groups):
        with group_tabs[idx]:
            st.subheader(f"Sociogram and Analysis for Group {group}")
            group_data = data[data['Group'] == group]
            G = create_graph(group_data)
            profiles = analyze_profiles(G)
            draw_graph(G, profiles)
            display_recommendations(profiles)
            calculate_group_metrics(G)

