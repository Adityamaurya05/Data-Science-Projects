import streamlit as st
import pandas as pd
import folium
from folium.plugins import MarkerCluster
from streamlit_folium import folium_static
from geopy.distance import geodesic
import plotly.express as px
import os
from collections import defaultdict, deque

# Define the path to your CSV file
CSV_PATH = r"Delhi metro.csv"

# Function to load data with error handling
@st.cache_data
def load_data(file_path):
    try:
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"The file {file_path} does not exist.")
        df = pd.read_csv(file_path)
        
        expected_columns = [
            'ID (Station ID)', 'Station Names', 'Dist. From First Station(km)', 
            'Metro Line', 'Opened(Year)', 'Layout', 'Latitude', 'Longitude'
        ]
        if not all(col in df.columns for col in expected_columns):
            missing = [col for col in expected_columns if col not in df.columns]
            raise KeyError(f"Missing columns in CSV: {missing}")
        
        df = df.rename(columns={
            'ID (Station ID)': 'Station ID',
            'Station Names': 'Station Name',
            'Dist. From First Station(km)': 'Distance from Start (km)',
            'Metro Line': 'Line',
            'Opened(Year)': 'Opening Date',
            'Layout': 'Station Layout'
        })
        
        df['Opening Date'] = pd.to_datetime(df['Opening Date'], dayfirst=True, errors='coerce')
        df['Station_Base_Name'] = df['Station Name'].str.replace(r'\s*\[Conn:.*\]', '', regex=True)
        return df
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return None

# Load the dataset
df = load_data(CSV_PATH)
if df is None:
    st.stop()

# Identify interchange stations
interchange_stations = df.groupby('Station_Base_Name')['Line'].nunique()
interchange_stations = interchange_stations[interchange_stations > 1].index.tolist()

# Define color mapping for metro lines
line_colors = {
    'Red line': 'red',
    'Yellow line': 'yellow',
    'Blue line': 'blue',
    'Blue line branch': 'blue',
    'Green line': 'green',
    'Green line branch': 'green',
    'Violet line': 'purple',
    'Pink line': 'pink',
    'Magenta line': 'darkred',
    'Orange line': 'orange',
    'Gray line': 'gray',
    'Aqua line': 'lightblue',
    'Rapid Metro': 'cadetblue'
}

# Build adjacency list for the metro network
def build_graph(df):
    graph = defaultdict(list)
    for line in df['Line'].unique():
        line_df = df[df['Line'] == line].sort_values('Distance from Start (km)')
        stations = line_df['Station_Base_Name'].tolist()
        for i in range(len(stations) - 1):
            graph[stations[i]].append((stations[i + 1], line))
            graph[stations[i + 1]].append((stations[i], line))
    
    for station in interchange_stations:
        lines = df[df['Station_Base_Name'] == station]['Line'].unique()
        for i in range(len(lines)):
            for j in range(i + 1, len(lines)):
                graph[station].append((station, f"Transfer from {lines[i]} to {lines[j]}"))
                graph[station].append((station, f"Transfer from {lines[j]} to {lines[i]}"))
    
    return graph

# Find route using BFS
def find_route(graph, start, end):
    if start == end:
        return [start], 0, []
    
    visited = set()
    queue = deque([(start, [start], 0, [])])
    while queue:
        current, path, distance, transfers = queue.popleft()
        if current == end:
            return path, distance, transfers
        
        if current not in visited:
            visited.add(current)
            for next_station, line_or_transfer in graph[current]:
                new_distance = distance
                new_transfers = transfers[:]
                
                if "Transfer" in line_or_transfer:
                    new_transfers.append(line_or_transfer)
                else:
                    current_dist = df[(df['Station_Base_Name'] == current) & (df['Line'] == line_or_transfer)]['Distance from Start (km)'].iloc[0]
                    next_dist = df[(df['Station_Base_Name'] == next_station) & (df['Line'] == line_or_transfer)]['Distance from Start (km)'].iloc[0]
                    new_distance += abs(next_dist - current_dist)
                
                new_path = path + [next_station] if next_station != current else path
                queue.append((next_station, new_path, new_distance, new_transfers))
    
    return None, 0, []

# Custom CSS for styling
st.markdown("""
    <style>
    .stTabs [data-baseweb="tab-list"] {
        border-bottom: 1px solid #333;
        background-color: #000;
        margin-bottom: 10px;
    }
    .stTabs [data-baseweb="tab"] {
        background-color: #000;
        color: white;
        padding: 10px 20px;
        margin-right: 5px;
        border-radius: 5px 5px 0 0;
        border: 1px solid #333;
        border-bottom: none;
    }
    .stTabs [data-baseweb="tab"]:hover {
        background-color: #333;
        color: white;
    }
    .stTabs [data-baseweb="tab"][aria-selected="true"] {
        background-color: #333;
        border-bottom: 1px solid #333;
        color: white;
    }
    .stContainer {
        padding: 20px;
        border: 1px solid #ccc;
    }
    .station-details {
        margin-left: 20px;
    }
    .tab-content {
        padding-top: 50px;
    }
    </style>
""", unsafe_allow_html=True)

# Build the metro graph
metro_graph = build_graph(df)

# Streamlit app with tabs
st.title("Delhi MetroNav Dashboard")
st.markdown("<hr>", unsafe_allow_html=True)

tab1, tab2 = st.tabs(["Dashboard", "Route Finder"])

# Tab 1: Dashboard
with tab1:
    st.markdown('<div class="tab-content">', unsafe_allow_html=True)

    st.sidebar.header("Filters")
    selected_line = st.sidebar.selectbox("Select Metro Line", df['Line'].unique())
    selected_station = st.sidebar.selectbox("Select Station", sorted(df['Station_Base_Name'].unique()))
    layout_filter = st.sidebar.multiselect("Filter by Layout", df['Station Layout'].unique(), default=df['Station Layout'].unique())
    year_filter = st.sidebar.slider(
        "Filter by Opening Year",
        int(df['Opening Date'].dt.year.min()),
        int(df['Opening Date'].dt.year.max()),
        (int(df['Opening Date'].dt.year.min()), int(df['Opening Date'].dt.year.max()))
    )

    filtered_df = df[
        (df['Line'] == selected_line) &
        (df['Station Layout'].isin(layout_filter)) &
        ((df['Opening Date'].dt.year >= year_filter[0]) & (df['Opening Date'].dt.year <= year_filter[1]) | df['Opening Date'].isna())
    ]

    st.subheader("Station Map")
    m = folium.Map(location=[28.6139, 77.2090], zoom_start=10)
    marker_cluster = MarkerCluster().add_to(m)
    for idx, row in df.iterrows():
        station_name = row['Station_Base_Name']
        line = row['Line']
        color = line_colors.get(line, 'gray')
        icon = folium.Icon(
            color=color,
            icon='star' if station_name in interchange_stations else 'circle',
            prefix='fa'
        )
        folium.Marker(
            location=[row['Latitude'], row['Longitude']],
            popup=f"{row['Station Name']} ({row['Line']})",
            icon=icon
        ).add_to(marker_cluster)
    folium_static(m, width=800, height=400)

    st.subheader("Station Details")
    station_data = df[df['Station_Base_Name'] == selected_station]
    if not station_data.empty:
        st.markdown('<div class="station-details">', unsafe_allow_html=True)
        st.write(f"**Station Name:** {selected_station}")
        st.write(f"**Lines:** {', '.join(station_data['Line'].unique())}")
        st.write(f"**Layout:** {station_data['Station Layout'].iloc[0]}")
        opening_date = station_data['Opening Date'].iloc[0]
        st.write(f"**Opening Date:** {opening_date.date() if pd.notna(opening_date) else 'Not Available'}")
        st.write(f"**Coordinates:** {station_data['Latitude'].iloc[0]}, {station_data['Longitude'].iloc[0]}")
        st.write("**Distance from Start (km):**")
        for line in station_data['Line'].unique():
            dist = station_data[station_data['Line'] == line]['Distance from Start (km)'].iloc[0]
            st.write(f"- {line}: {dist:.2f} km")
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.write(f"No details found for {selected_station}.")

    st.subheader(f"{selected_line} Statistics")
    line_stations = filtered_df.sort_values('Distance from Start (km)')
    if not line_stations.empty:
        total_stations = len(line_stations)
        total_length = line_stations['Distance from Start (km)'].max()
        avg_distance = line_stations['Distance from Start (km)'].diff().mean() if total_stations > 1 else 0
        st.write(f"**Total Stations:** {total_stations}")
        st.write(f"**Total Length:** {total_length:.2f} km")
        st.write(f"**Average Distance Between Stations:** {avg_distance:.2f} km")
    else:
        st.write(f"No stations found for {selected_line} with the current filters.")

    st.subheader("Overall Statistics")
    total_unique_stations = df['Station_Base_Name'].nunique()
    st.write(f"**Total Unique Stations:** {total_unique_stations}")
    layout_dist = df['Station Layout'].value_counts()
    fig = px.pie(layout_dist, values=layout_dist.values, names=layout_dist.index, title="Station Layout Distribution")
    st.plotly_chart(fig, use_container_width=True)

    st.markdown('</div>', unsafe_allow_html=True)

# Tab 2: Route Finder
with tab2:
    st.header("Find Your Metro Route")
    
    start_station = st.selectbox("Select Starting Station", sorted(df['Station_Base_Name'].unique()), key="start")
    dest_station = st.selectbox("Select Destination Station", sorted(df['Station_Base_Name'].unique()), key="dest")
    
    if st.button("Find Route"):
        if start_station == dest_station:
            st.write(f"**Route:** You are already at {start_station}!")
        else:
            route, total_distance, transfers = find_route(metro_graph, start_station, dest_station)
            if route:
                # Create two columns: left for text, right for map
                col1, col2 = st.columns([1, 1])  # Equal width columns

                with col1:
                    # Textual Route Display
                    st.write(f"**Route:**")
                    current_line = None
                    transfer_count = 0
                    
                    for i, station in enumerate(route):
                        if i > 0:
                            for next_station, line_or_transfer in metro_graph[route[i-1]]:
                                if next_station == station and "Transfer" not in line_or_transfer:
                                    new_line = line_or_transfer
                                    if current_line and current_line != new_line:
                                        transfer_count += 1
                                        st.write(f"↓ At {station}: Transfer from {current_line} to {new_line} (Total Transfers: {transfer_count})")
                                    current_line = new_line
                                    break
                        
                        if i == 0 or station != route[i-1]:
                            line_display = f" ({current_line})" if current_line else ""
                            st.write(f"↓ {station}{line_display}")
                        elif station == route[i-1] and i < len(route) - 1 and station == route[i+1]:
                            for transfer in transfers:
                                if transfer in [t for _, t in metro_graph[station] if route[i+1] == station]:
                                    transfer_count += 1
                                    st.write(f"↓ At {station}: {transfer} (Total Transfers: {transfer_count})")
                                    current_line = transfer.split(" to ")[-1]
                    
                    st.write(f"**Total Distance:** {total_distance:.2f} km")
                    st.write(f"**Number of Stations:** {len(route)}")
                    st.write(f"**Total Transfers:** {transfer_count}")

                with col2:
                    # Route Map
                    st.subheader("Route Map")
                    m = folium.Map(location=[28.6139, 77.2090], zoom_start=10)
                    marker_cluster = MarkerCluster().add_to(m)

                    # Plot all stations
                    for idx, row in df.iterrows():
                        station_name = row['Station_Base_Name']
                        line = row['Line']
                        color = line_colors.get(line, 'gray')
                        icon = folium.Icon(
                            color=color,
                            icon='star' if station_name in interchange_stations else 'circle',
                            prefix='fa'
                        )
                        folium.Marker(
                            location=[row['Latitude'], row['Longitude']],
                            popup=f"{row['Station Name']} ({row['Line']})",
                            icon=icon
                        ).add_to(marker_cluster)

                    # Highlight the route
                    route_coords = []
                    current_line = None
                    for i, station in enumerate(route):
                        if i > 0:
                            for next_station, line_or_transfer in metro_graph[route[i-1]]:
                                if next_station == station and "Transfer" not in line_or_transfer:
                                    current_line = line_or_transfer
                                    break
                        station_data = df[(df['Station_Base_Name'] == station) & (df['Line'] == current_line)]
                        if not station_data.empty:
                            lat, lon = station_data['Latitude'].iloc[0], station_data['Longitude'].iloc[0]
                            route_coords.append([lat, lon])
                        if i < len(route) - 1 and station == route[i+1]:
                            for transfer in transfers:
                                if transfer in [t for _, t in metro_graph[station] if route[i+1] == station]:
                                    new_line = transfer.split(" to ")[-1]
                                    new_station_data = df[(df['Station_Base_Name'] == station) & (df['Line'] == new_line)]
                                    if not new_station_data.empty:
                                        lat, lon = new_station_data['Latitude'].iloc[0], new_station_data['Longitude'].iloc[0]
                                        route_coords.append([lat, lon])
                                    current_line = new_line
                                    break

                    folium.PolyLine(
                        locations=route_coords,
                        weight=5,
                        color='black',
                        opacity=0.8
                    ).add_to(m)

                    if route_coords:
                        m.fit_bounds(route_coords)

                    folium_static(m, width=400, height=400)  # Adjust width for side-by-side layout
            else:
                st.error("No route found between the selected stations.")