import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os
import warnings
import graphviz
import folium
import geopandas as gpd
from streamlit_folium import st_folium
from graphviz import Digraph

import importlib.util
import sys
from pathlib import Path

# CUSTOMIZE FUN APP COLORS HERE:
st.markdown(
    """
    <style>
    /* Main page background color */
    .stApp {
        background-color: #2f3338;
    }
    /* Sidebar background color */
    [data-testid="stSidebar"] {
        background-color: #082047;
    }
    /* Title text color */
    .stTitle {
        color: #000000;
    }
    </style>
    """,
    unsafe_allow_html=True
)

warnings.filterwarnings("ignore")



st.title('ICE-AGE Research Methods')
st.markdown('This page will describe the flow and methods to __________')

st.sidebar.title("Customize Map Appearance")
map_style = st.sidebar.selectbox(
    "Select Map Style", 
    options=["CartoDB positron", "CartoDB dark_matter"],
    index=0  # Default style: CartoDB positron
)

st.sidebar.image("Iceberg-images/Calving-streamlit.png", caption = "An iceberg towers above the waters of Ilulissat Icefjord, after calving off of Sermeq Kujalleq, or Jakobshavn Glacier, in western Greenland. Credit: Allen Pope, NSIDC")
st.sidebar.image("Iceberg-images/Boats-n-icebergs-streamlit.png", caption= "A scientific research vessel churns through the coastal waters of western Greenland, leaving an open path through small icebergs and bergy bits. Instruments deployed in the region help researchers to better understand ocean conditions and how narwhal whales use the glacial fjord environment. Credit: Twila Moon, NSIDC")
#CUSTOMIZE GREENLAND MAP HERE: 
st.title("🗺️ Map of Greenland with selected study sites:")
csv_file_path = "/workspaces/Greenland-icebergmeltrate-interactive/Glacier-Locations.csv"
natural_earth_path = "/workspaces/Greenland-icebergmeltrate-interactive/ne_110m_admin_0_countries.zip"

def create_interactive_map(glacier_sites, map_style):
    # Load Natural Earth dataset
    world = gpd.read_file(natural_earth_path)
    greenland = world[world['NAME'] == 'Greenland']

    # Convert Greenland to GeoJSON for Folium
    greenland_geojson = greenland.to_crs("EPSG:4326").__geo_interface__
    m = folium.Map(location=[72, -40], zoom_start=4, tiles=map_style)  # Use the selected map style

    # Greenland shapefile
    folium.GeoJson(
        greenland_geojson,
        name="Greenland",
        style_function=lambda x: {"fillColor": "#05faac", "color": "black", "weight": 1.0},
    ).add_to(m)

    # Colors for specific regions
    region_colors = {
        'SE': 'red', 
        'CE': 'orange', 
        'CW': 'yellow', 
        'NW': 'green', 
        'NE': 'lime', 
        'NO': 'blue', 
        'SW': 'purple' 
    }

    # Add glacier sites as markers
    for _, site in glacier_sites.iterrows():
        region = site['Region'] 
        color = region_colors.get(region, 'red')  

        folium.Marker(
            location=[site['LAT'], site['LON']],
            popup=f"Official Name: {site['Official_n']}",
            icon=folium.Icon(color=color, icon="info-sign"),
        ).add_to(m)

    return m


try:
    glacier_sites = pd.read_csv(csv_file_path)
    required_columns = {'LAT', 'LON', 'Official_n', 'Glacier_ID', 'Region'}
    if not required_columns.issubset(glacier_sites.columns):
        st.error(f"The uploaded file must contain the following columns: {', '.join(required_columns)}")
    else:
        interactive_map = create_interactive_map(glacier_sites, map_style)  # Pass the selected map style
        st_folium(interactive_map, width=800, height=600)
except Exception as e:
    st.error(f"An error occurred while loading the CSV file: {e}")

#CUSTOMIZE INFORMATION ABOUT SAMPLING HERE: 
st.markdown("""
            Based on the region, we were able to choose (date pairings - Think about a better way to phrase this) with varying time spacing.   
            - Northern region: Bi-monthly spacing
            - Central regions: Monthly spacing
            - SouthEastern region: Weekly spacing
            - SouthWestern region: Bi-weekly spacing
""")
st.markdown("\n\n")

import streamlit as st
from graphviz import Digraph

# Create a Digraph object
dot = Digraph()

# Set the graph size (increase as needed)
dot.attr(size='80,100')  # Adjust the size
dot.attr(dpi='65')  # Optional: Increase resolution for better clarity

# Add nodes
dot.node('A', 'Worldview stereo images', shape='rect', style='filled', fillcolor='lightblue')
dot.node('B', 'DEMs generation by NASA Ames Stereo Pipeline (ASP)', shape='rect', style='filled', fillcolor='lightblue')
dot.node('C', 'Manual iceberg tracking', shape='rect', style='filled', fillcolor='lightblue')
dot.node('D', 'Differencing DEMs', shape='rect', style='filled', fillcolor='lightblue')
dot.node('E', 'Compute Volume Change', shape='rect', style='filled', fillcolor='lightblue')
dot.node('F', 'Subtract surface melting from volume change ', shape='rect', style='filled', fillcolor='lightblue')
dot.node('G', 'Freshwater flux from submarine melting', shape='rect', style='filled', fillcolor='lightblue')
dot.node('H', 'melt rate = freshwater flux / submerged area ', shape='rect', style='filled', fillcolor='lightblue')


dot.edges(['AB', 'BC', 'CD', 'DE', 'EF', 'FG', 'GH'])
col1 = st.container()
with col1:
    st.graphviz_chart(dot)
    st.image("Iceberg-images/Aman-cool-scientist.png", caption="Woot woot", use_container_width=True)  # Replace with your image path


st.title("Data Generation:")
