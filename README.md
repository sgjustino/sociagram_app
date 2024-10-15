# Sociogram Visualizer and Relationship Analysis

This Streamlit app provides an interactive sociogram visualizer to analyze group dynamics using sociometric data. It categorizes individuals into specific profiles (Isolates, Solitary, Stars, Cliques, and Interconnectors) based on their connections and calculates metrics to understand group cohesion and communication flow.

## Features

1. **Group Selection with Scrollable Tabs**:
   - Navigate across groups with scrollable tabs for numerous groups.

2. **Sociogram Visualization**:
   - Visualizes group dynamics as a sociogram.
   - Nodes represent individuals, and edges represent their relationships, with custom color-coding for each profile type.

3. **Profile Analysis and Definitions with Interventions**:
   - Individuals are categorized into relationship profiles based on network characteristics:
     - **Isolates**: Individuals with no connections in the group, defined as nodes with zero in-degree and out-degree.
       - **Intervention**: Provide structured group activities and encourage active interaction with more engaged members to help them feel integrated.
     - **Solitary**: Individuals with incoming connections but no outgoing connections, suggesting one-sided relationships.
       - **Intervention**: Encourage these individuals to participate actively in discussions and activities, fostering reciprocal relationships.
     - **Stars**: Highly connected individuals with at least 4 incoming connections, indicating popularity or influence.
       - **Utility**: Stars can be role models or facilitators in group settings, promoting inclusivity and helping others feel welcome.
     - **Cliques**: Individuals who are part of mutually connected groups within the same community (detected via Louvain clustering).
       - **Intervention**: Break down clique barriers by introducing mixed-group activities or collaborative projects with other clusters.
     - **Interconnectors**: Individuals who act as "bridges" between different clusters by connecting with members across at least 3 distinct communities.
       - **Utility**: Leverage interconnectors as peer support leaders or liaisons to foster communication and cohesion across communities.

### How Community Detection with Louvain Method Works

The Louvain method is a community detection algorithm that identifies clusters of individuals (communities) that are more densely connected internally. It works by maximizing **modularity**, a measure that quantifies the density of links within communities compared to links between communities.

- **How It Works**: 
  - Each individual starts as its own community, then individuals are iteratively grouped to maximize modularity.
  - Individuals within the same community are more likely to have dense interconnections, indicating a tightly-knit sub-group within the larger network.

### How Profiles Are Defined with Louvain Communities

- **Cliques**: Groups of individuals within the same Louvain-detected community of size 3 or larger. In these cliques, every individual is directly connected to every other individual in the group. Cliques often represent closely connected friend groups.
- **Interconnectors**: Individuals that link with members across at least 3 distinct Louvain communities, serving as bridges and enhancing communication across otherwise separate clusters.

4. **Group Cohesion Metrics with Interventions**:
   - Each group’s network structure is analyzed to calculate key metrics, with potential interventions suggested based on the metric values:
   
     - **Connectedness**: Measures the percentage of observed connections relative to the maximum possible connections.
       - **Formula**: `(Actual Connections / Maximum Possible Connections) * 100`
       - **Interpretation**: High connectedness indicates an actively engaged group; low connectedness may suggest isolation or limited interactions.
       - **Maximum Possible Connections**: For each individual who can select up to 3 friends, the maximum possible connections for a group of `N` members is `3 * N`.
       - **Intervention**: If connectedness is low, initiate more team-building activities to increase interaction.

     - **Reciprocity**: Indicates the percentage of friendships that are mutual.
       - **Formula**: `(Mutual Connections / Maximum Possible Mutual Connections) * 100`
       - **Interpretation**: High reciprocity suggests balanced, reciprocated relationships; low reciprocity may indicate one-sided friendships.
       - **Maximum Possible Mutual Connections**: For a group of size `N` where each individual can choose up to 3 friends, the maximum possible mutual connections is half of the total maximum possible connections, i.e., `1.5 * N`.
       - **Intervention**: If reciprocity is low, encourage open dialogue and active partnership to foster mutual relationships and balanced connections.

     - **Reachability**: Reflects the proportion of group members reachable (directly or indirectly) within the largest weakly connected component.
       - **Formula**: `(Size of Largest Connected Component / Total Number of Nodes) * 100`
       - **Interpretation**: High reachability indicates cohesion, while low reachability suggests fragmentation.
       - **Largest Weakly Connected Component**: The largest subset of nodes where each node is reachable from any other node in the component, ignoring edge directions.
       - **Intervention**: Low reachability can be addressed by increasing communication and collaboration among isolated nodes or fragmented groups, possibly by pairing them with interconnectors.

     - **Speed of Communication**: Calculates the reach within a 3-step radius from the most connected individual, showing how quickly information can spread.
       - **Formula**: `(Nodes Reachable within 3 Steps from Most Connected Node / Total Number of Nodes) * 100`
       - **Interpretation**: High values indicate efficient communication; low values suggest limited reach within a few steps.
       - **Most Connected Node**: The node with the highest degree (sum of in-degree and out-degree) within the largest weakly connected component.
       - **Intervention**: For low speed of communication, consider designating roles to Stars and Interconnectors to expedite information flow and ensure everyone is informed while being conscious of isolated individuals.

## Getting Started

1. **Run the App**: Launch the Streamlit app with the following command:
   ```bash
   streamlit run app.py
   ```

2. **Upload Data**: Upload a CSV file with the following structure:
   - **Group**: Group ID.
   - **Select your Number**: Unique identifier for each individual.
   - **Select Close Friend 1**: ID of the first close friend.
   - **How close are you to Close Friend 1?**: Strength of connection to the first friend.
   - **Select Close Friend 2**: ID of the second close friend.
   - **How close are you to Close Friend 2?**: Strength of connection to the second friend.
   - **Select Close Friend 3**: ID of the third close friend.
   - **How close are you to Close Friend 3?**: Strength of connection to the third friend.

3. **Example CSV Format**:
   ```csv
   Group,Select your Number,Select Close Friend 1,How close are you to Close Friend 1?,Select Close Friend 2,How close are you to Close Friend 2?,Select Close Friend 3,How close are you to Close Friend 3?
   G1,1,2,5,3,4,4,3
   G1,2,3,3,1,5,5,4
   G1,3,1,4,2,4,6,2
   ...
   ```
