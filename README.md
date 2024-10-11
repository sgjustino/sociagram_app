# Sociogram Visualizer and Relationship Analysis

This Streamlit app provides an interactive sociogram visualizer to analyze group dynamics using sociometric data. It categorizes individuals into specific profiles (Isolates, Solitary, Stars, Cliques, and Interconnectors) based on their connections and calculates metrics to understand group cohesion and communication flow.

## Features

1. **Group Selection with Scrollable Tabs**:
   - Navigate across groups with scrollable tabs that support up to 20+ groups.
2. **Sociogram Visualization**:
   - Visualizes group dynamics as a sociogram using NetworkX and Matplotlib.
   - Nodes represent individuals, and edges represent their relationships, with custom color-coding for each profile type.

3. **Profile Analysis and Definitions**:
   - Individuals are categorized into relationship profiles based on network characteristics:
     - **Isolates**: Individuals with no connections in the group, defined as nodes with zero in-degree and out-degree.
     - **Solitary**: Individuals with incoming connections but no outgoing connections, suggesting one-sided relationships.
     - **Stars**: Highly connected individuals with at least 4 incoming connections, indicating popularity or influence.
     - **Cliques**: Individuals who are part of mutually connected groups within the same community (detected via Louvain clustering) and have at least 3 mutual connections.
     - **Interconnectors**: Individuals who act as "bridges" between different clusters by connecting with members across at least 3 distinct communities.

   Each profile is accompanied by tailored recommendations to encourage social cohesion and enhance group dynamics.

4. **Group Cohesion Metrics**:
   - Each group’s network structure is analyzed to calculate key metrics:
     - **Connectedness**: Measures the percentage of observed connections relative to the maximum possible connections.
       - **Formula**: `(Actual Connections / Maximum Possible Connections) * 100`
       - **Interpretation**: High connectedness indicates an actively engaged group, while low connectedness may suggest isolation or limited interactions.
     - **Reciprocity**: Indicates the percentage of friendships that are mutual.
       - **Formula**: `(Mutual Connections / Maximum Possible Mutual Connections) * 100`
       - **Interpretation**: High reciprocity suggests balanced, reciprocated relationships, while low reciprocity may imply one-sided friendships.
     - **Reachability**: Reflects the proportion of group members reachable (directly or indirectly) within the largest weakly connected component.
       - **Formula**: `(Size of Largest Connected Component / Total Number of Nodes) * 100`
       - **Interpretation**: High reachability means most members are accessible, promoting cohesion, while low reachability indicates fragmentation.
     - **Speed of Communication**: Calculates the reach within a 3-step radius from the most connected individual, showing how quickly information can spread.
       - **Formula**: `(Nodes Reachable within 3 Steps from Most Connected Node / Total Number of Nodes) * 100`
       - **Interpretation**: High values indicate efficient communication, while low values suggest limited reach within a few steps.

## Getting Started

1. **Run the App**: Launch the Streamlit app with the following command:
   ```bash
   streamlit run sociagram_app.py
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