import streamlit as st
import zipfile
import os
import folium
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import numpy as np
import contextily as ctx
import glob
import graphviz
import warnings

from streamlit_folium import st_folium
from shapely.affinity import translate


st.markdown(
    """
    <style>
    /* Main page background color */
    .stApp {
        background-color: #2d526e;
    }
    /* Sidebar background color */
    [data-testid="stSidebar"] {
        background-color: #2e3a5c;
    }
    /* Title text color */
    .stTitle {
        color: #00695c;
    }
    </style>
    """,
    unsafe_allow_html=True
)
warnings.filterwarnings("ignore")


##CUSTOMIZE SIDEBAR HERE: 
#st.sidebar.header('Sidebar goes here')
#st.sidebar.markdown('All relevant information goes here!')
st.sidebar.image("Greenland-glacier-placeholder.webp") #caption = "Get pictures from Twila for this!")
st.sidebar.image('Greenland-placeholder-2.jpg')
#st.sidebar.image('Opa.jpg', caption = '🧡My child for a placeholder🧡')

st.sidebar.title("Customize Map Appearance")
map_style = st.sidebar.selectbox(
    "Select Map Style", 
    options=["CartoDB positron", "CartoDB dark_matter"],
    index=0  # Default style: CartoDB positron
)


#CUSTOMIZE TITLE FOR APP HERE: 
st.title('🧊An Iceberg Catalog for Analysis of Greenland Environments: ICE-AGE')
st.markdown('')
st.title("❄️Purpose:")
st.markdown("This application will allow you to visualize manually delineated icebergs from Greenlandic fjords. ")
st.info("🏔️Data source: ")

#CUSTOMIZE FLOW CHART HERE: 
st.title('🌊Research Workflow')
dot = graphviz.Digraph(comment='Workflow', graph_attr={'rankdir': 'LR'})  # 'LR' makes it horizontal

dot.node('A', 'Start', shape='rect',style = 'filled',fillcolor = 'lightblue')  # Square nodes
dot.node('B', '1', shape='rect',style = 'filled',fillcolor = 'lightblue')
dot.node('C', '2', shape='rect',style = 'filled',fillcolor = 'lightblue')
dot.node('D', '3', shape='rect',style = 'filled',fillcolor = 'lightblue')
dot.node('E', 'End', shape = 'rect',style = 'filled',fillcolor = 'lightblue')
dot.edges(['AB', 'BC', 'CD','DE'])
st.graphviz_chart(dot)

#CUSTOMIZE INFORMATION ABOUT SAMPLING HERE: 
st.markdown("""
            Based on the region, we were able to choose (date pairings - Think about a better way to phrase this) with varying time spacing.   
            - Northern region: Bi-monthly spacing
            - Central regions: Monthly spacing
            - SouthEastern region: Weekly spacing
            - SouthWestern region: Bi-weekly spacing
""")

#CUSTOMIZE GREENLAND MAP HERE: 
st.title("🗺️ Map of Greenland with selected study sites:")
csv_file_path = "/workspaces/Greenland-icebergmeltrate-interactive-1/Glacier-Locations.csv"
natural_earth_path = "/workspaces/Greenland-icebergmeltrate-interactive-1/ne_110m_admin_0_countries.zip"

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



#CUSTOMIZE THE ICEBERG SHAPEFILE VIEWER HERE: 
st.title("🔍👀Iceberg Shapefile Viewer:")
st.markdown('⏳Note: The Iceberg Shape Comparison chart may take a moment to load!')
st.info('Click here for the [Fjord Abbreviation List & Paired Dates](https://docs.google.com/spreadsheets/d/1kCcKqf717kK3_Xx-GDe0f61jhlUpZ5n6BN1qtiw7S4w/edit?gid=0#gid=0)')

base_path = "Iceberg-shapefiles"
if os.path.exists(base_path):
    site_names = [name for name in os.listdir(base_path) if os.path.isdir(os.path.join(base_path, name))]

    site_name = st.selectbox("Select Site Name", site_names)
else:
    st.error(f"Base path '{base_path}' does not exist. Please check your folder structure.")

early_date = st.text_input("Enter the earlier date (YYYYMMDD):")
late_date = st.text_input("Enter the later date (YYYYMMDD):")

if site_name and early_date and late_date:
    date_range_folder = f"{early_date}-{late_date}"
    target_folder = os.path.join(base_path, site_name, date_range_folder)

    if os.path.exists(target_folder):
        shapefiles = [f for f in os.listdir(target_folder) if f.endswith('.shp')]

        if shapefiles:
            st.subheader(f"Displaying {len(shapefiles)} Shapefiles")

            max_width, max_height = 0, 0
            shapefile_metadata = []
            area_data = []

            for filename in shapefiles:
                shapefile_path = os.path.join(target_folder, filename)
                gdf = gpd.read_file(shapefile_path)

                if gdf.crs is None:
                    gdf = gdf.set_crs('EPSG:3413')
                gdf = gdf.to_crs('EPSG:3413')

                if not gdf.empty:
                    overall_bounds = gdf.total_bounds
                    width = overall_bounds[2] - overall_bounds[0]
                    height = overall_bounds[3] - overall_bounds[1]
                    max_width = max(max_width, width)
                    max_height = max(max_height, height)

                    area = gdf.area.sum() 
                    area_data.append(area)

                    shapefile_metadata.append((filename, gdf, width, height))

            num_columns = 3
            cols = st.columns(num_columns)

            for i, (filename, gdf, width, height) in enumerate(shapefile_metadata):
                col = cols[i % num_columns]
                with col:
                    fig, ax = plt.subplots(figsize=(6, 6))
                    color = '#f5a442' if early_date in filename else '#8bc34a'

                    overall_bounds = gdf.total_bounds
                    gdf['geometry'] = gdf['geometry'].apply(lambda geom: translate(geom, -overall_bounds[0], -overall_bounds[1]))

                    gdf.plot(ax=ax, color=color, edgecolor='black', alpha=0.8, linewidth=2)

                    ax.set_xlim(0, max_width)
                    ax.set_ylim(0, max_height)
                    ax.set_xlabel("Width (m)")
                    ax.set_ylabel("Height (m)")
                    ax.set_title(filename, fontsize=10)
                    ax.axis("on")

                    st.pyplot(fig)

            #SHAPEFILE TABLE BELOW: 
            area_df = pd.DataFrame({"Shapefile": shapefiles, "Area (m²)": area_data})
            st.subheader("Iceberg Area Information:")
            st.dataframe(area_df)

        else:
            st.error(f"No shapefiles found in the folder: {target_folder}")
    else:
        st.error(f"Target folder '{target_folder}' does not exist. Please check the dates and site name.")
else:
    st.info("Please select a site name, enter both dates, and hit enter to proceed!")

 #THIS FUNCTION WILL FIND THE DOMINANT ANGLE:    
def calculate_dominant_angle(gdf):
    """Calculate the dominant angle for the geometry in the shapefile."""
    gdf = gdf[gdf['geometry'].is_valid]  # Ensure geometry is valid
    bounds = gdf['geometry'].apply(lambda geom: geom.minimum_rotated_rectangle)
    
    def longest_edge_angle(box):
        coords = np.array(box.exterior.coords)
        edges = np.diff(coords, axis=0)[:-1]  # Skip closing edge
        lengths = np.linalg.norm(edges, axis=1)
        longest_idx = np.argmax(lengths)
        longest_edge = edges[longest_idx]
        angle = np.arctan2(longest_edge[1], longest_edge[0])
        return np.degrees(angle)
    
    angles = bounds.apply(longest_edge_angle)
    return angles.mean()  # Use the average dominant angle

#CUSTOMIZE QUARTILE BASED ICEBERG SHAPE COMPARISON HERE: 
st.title("📊 Quartile-Based Iceberg Shape Comparison")
area_df["Quartile"] = pd.qcut(area_df["Area (m²)"], 4, labels=["Q1", "Q2", "Q3", "Q4"])

quartile_colors = {"Q1": "#8bd67a", "Q2": "#e080d7", "Q3": "#f7bf07", "Q4": "#f78307"}
quartile_opacity = {"Q1": 0.4, "Q2": 0.4, "Q3": 0.4, "Q4": 0.4}

# Determine global plot limits for consistent scaling
max_width, max_height = 0, 0
for shapefile in area_df["Shapefile"]:
    shapefile_path = os.path.join(target_folder, shapefile)
    gdf = gpd.read_file(shapefile_path)
    
    if gdf.crs is None:
        gdf = gdf.set_crs('EPSG:3413')
    gdf = gdf.to_crs('EPSG:3413')
    
    if not gdf.empty:
        bounds = gdf.total_bounds
        max_width = max(max_width, bounds[2] - bounds[0])
        max_height = max(max_height, bounds[3] - bounds[1])

# Prepare subplots for quartile overlays
fig, axes = plt.subplots(2, 2, figsize=(12, 12), sharex=True, sharey=True)
axes = axes.flatten()

for i, quartile in enumerate(["Q1", "Q2", "Q3", "Q4"]):
    ax = axes[i]
    ax.set_title(f"Quartile {quartile}", fontsize=10)
    
    quartile_files = area_df[area_df["Quartile"] == quartile]["Shapefile"]
    
    for shapefile in quartile_files:
        shapefile_path = os.path.join(target_folder, shapefile)
        gdf = gpd.read_file(shapefile_path)
        
        if gdf.crs is None:
            gdf = gdf.set_crs('EPSG:3413')
        gdf = gdf.to_crs('EPSG:3413')
        
        if not gdf.empty:
            # Calculate dominant angle
            dominant_angle = calculate_dominant_angle(gdf)
            
            # Rotate geometry by -dominant_angle to align horizontally
            gdf["geometry"] = gdf["geometry"].rotate(-dominant_angle, origin="center")
            
            # Translate to origin for overlay
            overall_bounds = gdf.total_bounds
            gdf["geometry"] = gdf["geometry"].apply(lambda geom: translate(geom, -overall_bounds[0], -overall_bounds[1]))
            
            # Plot geometry
            gdf.plot(ax=ax, color=quartile_colors[quartile], alpha=quartile_opacity[quartile], edgecolor="black")
    
    ax.set_xlim(0, max_width)
    ax.set_ylim(0, max_height)
    ax.set_xlabel("Width (m)")
    ax.set_ylabel("Height (m)")
    ax.grid(visible=True, linestyle='--', linewidth=0.5)

st.pyplot(fig)


st.title("🥳Acknowledgements:")
st.markdown("""
            Our group is very committed to (mission statement )  
            Special thanks to: 
            - All you cool cats! (Fill out later)
""")
