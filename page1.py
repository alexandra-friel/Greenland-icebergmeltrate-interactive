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
        background-color: #2f3338;
    }
    /* Sidebar background color */
    [data-testid="stSidebar"] {
        background-color: #082047;
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
st.sidebar.image("Iceberg-images/Swirly-iceberg-streamlit.png", caption = "A sculpted Iceberg drifts off of Baffin Island, Nunavut. Icebergs form when chunks of ice calve, or break off, from glaciers, ice shelves, or a larger iceberg. The North Atlantic and the cold waters surrounding Antarctica are home to most of the icebergs on Earth. Credit: Shari Fox, NSIDC")
st.sidebar.image("Iceberg-images/Beautiful-icebergs-streamlit.png", caption = "Credit: Twila Moon, NSIDC")
#st.sidebar.image('Opal.jpg', caption = '🧡My child for a placeholder🧡')


#CUSTOMIZE TITLE FOR APP HERE: 
st.title("🔍👀Iceberg Shapefile Viewer:")
st.markdown('')
st.markdown("❄️This page will allow you to explore iceberg varying iceberg shapes and sizes using shapefiles. ")
st.markdown("The plots will automatically adjust the axis boundaries based on the largest iceberg, which ensures proper scaling for comparative analysis. The icebergs are color-coded by date, with orange representing the earlier date and green representing the later date.")
st.markdown("The shapefiles are then divided into four groups based on area, simplifying the identification of patterns in shape and size. Each group is displayed in its dedicated subplot, with overlapping shapes displayed  in low opacity. This will hopefully expose the trends and variations across groups while preserving individual details. ")



#CUSTOMIZE THE ICEBERG SHAPEFILE VIEWER HERE: 
st.info('Click here for the [Fjord Abbreviation List & Paired Dates](https://docs.google.com/spreadsheets/d/1kCcKqf717kK3_Xx-GDe0f61jhlUpZ5n6BN1qtiw7S4w/edit?gid=0#gid=0)')
st.markdown('⏳Note: The error area_df is not defined will be resolved once your input is complete!')


base_path = "Iceberg-shapefiles"
if os.path.exists(base_path):
    site_names = [name for name in os.listdir(base_path) if os.path.isdir(os.path.join(base_path, name))]

    site_name = st.selectbox("Select Site Name", site_names, key="site_name_selectbox")  # Add unique key
else:
    st.error(f"Base path '{base_path}' does not exist. Please check your folder structure.")

early_date = st.text_input("Enter the earlier date (YYYYMMDD):", key="early_date_input")  # Add unique key
late_date = st.text_input("Enter the later date (YYYYMMDD):", key="late_date_input")  # Add unique key

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
        
        color = quartile_colors[quartile]
        opacity = quartile_opacity[quartile]

        overall_bounds = gdf.total_bounds
        gdf['geometry'] = gdf['geometry'].apply(lambda geom: translate(geom, -overall_bounds[0], -overall_bounds[1]))

        gdf.plot(ax=ax, color=color, edgecolor='black', alpha=opacity, linewidth=2)
    
    ax.set_xlim(0, max_width)
    ax.set_ylim(0, max_height)
    ax.set_xlabel("Width (m)")
    ax.set_ylabel("Height (m)")

st.pyplot(fig)

