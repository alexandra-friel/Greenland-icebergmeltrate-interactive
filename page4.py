import streamlit as st
import pandas as pd
import geopandas as gpd
import folium
from streamlit_folium import st_folium
import os
import warnings

# Suppress CRS warning for missing EPSG
warnings.filterwarnings("ignore", message=".*CRS is None.*")

st.title("🗺️ Visualize iceberg spatial distributions")
st.markdown("This is an interactive map that will allow you to zoom into specific sites in order to visualize spatial distributions of icebergs in Greenland.")
# Sidebar image and information
st.sidebar.image("Iceberg-images/Glacier-iceberg-Streamlit.png", caption="An iceberg sits in Kongsfjord, with Midtre Lovénbreen in the background, at 79°N, in northern Svalbard. Located near the research town of Ny-Ålesund, it is an ideal location to study Arctic glaciology. Credit: Allen Pope, NSIDC")

st.info('Fill out the prompts in the sidebar to display the interactive map! Enjoy puffins while you wait. :)')
st.markdown('👆Click the icebergs to view information pertaining to iceberg width, height, etc.')
st.markdown('✋ Pan around the map to see how the icebergs have drifted!')
st.info('Click here for the [Fjord Abbreviation List & Paired Dates](https://docs.google.com/spreadsheets/d/1kCcKqf717kK3_Xx-GDe0f61jhlUpZ5n6BN1qtiw7S4w/edit?gid=0#gid=0)')

# Add placeholder for the GIF or animation
#gif_placeholder = st.empty()

# Display the penguin smack GIF
#gif_placeholder.markdown(
  #  """
  # <div style="display: flex; justify-content: center;">
     #   <img src="https://media.giphy.com/media/MZjgAkeenlkTKh5Ln5/giphy.gif" width="500">
   # </div>
  #  """,
   # unsafe_allow_html=True
#)
# File paths
csv_file_path = "/workspaces/Greenland-icebergmeltrate-interactive/Glacier-Locations.csv"
shapefile_base_path = "/workspaces/Greenland-icebergmeltrate-interactive/Iceberg-shapefiles"

# Function to load and reproject shapefile
def load_and_reproject_shapefile(filepath):
    gdf = gpd.read_file(filepath)
    if gdf.crs is None:
        gdf.set_crs("EPSG:3413", inplace=True)  # Set EPSG:3413 for Greenland's Polar Stereographic
    return gdf.to_crs("EPSG:4326")  # Reproject to EPSG:4326 for Folium compatibility

# Function to calculate width and height of the iceberg (bounding box)
def calculate_width_height(gdf):
    # Reproject to EPSG:3413 (meters)
    gdf = gdf.to_crs("EPSG:3413")
    
    # Get the bounding box of the iceberg shape in meters
    bounds = gdf.total_bounds
    width = bounds[2] - bounds[0]  # x_max - x_min (in meters)
    height = bounds[3] - bounds[1]  # y_max - y_min (in meters)
    
    # Return width and height rounded to 2 decimal places
    return round(width, 2), round(height, 2)

# Function to create interactive map
def create_interactive_map(glacier_sites, site_id, early_date, later_date, selected_icebergs, plot_all, plot_all_files):
    # Get site info
    site = glacier_sites[glacier_sites['Glacier_ID'] == site_id]
    site_lat, site_lon = site.iloc[0]['LAT'], site.iloc[0]['LON']
    
    # Initialize map
    m = folium.Map(location=[site_lat, site_lon], zoom_start=11.5, tiles="CartoDB positron")
    
    # Define color mapping for dates
    date_colors = {
        early_date: "blue",
        later_date: "green"
    }

    # Add iceberg shapefiles
    if plot_all_files:
        # Load all iceberg files from the "KAS-all" folder
        site_path = os.path.join(shapefile_base_path, f"{site_id}-all")
        if os.path.exists(site_path):
            shapefiles = [f for f in os.listdir(site_path) if f.endswith(".shp")]
            for iceberg in shapefiles:
                shp_path = os.path.join(site_path, iceberg)
                gdf = load_and_reproject_shapefile(shp_path)
                
                # Extract the date from the filename (assuming the date is part of the filename)
                # Modify this based on the filename structure; this is an example:
                date_in_filename = iceberg.split('-')[0]  # Assuming the first part of the filename is the date
                
                # Assign a color based on the date
                color = date_colors.get(date_in_filename, "gray")  # Default to gray if date is not recognized
                
                # Calculate width and height
                width, height = calculate_width_height(gdf)
                
                # Create popup with width and height
                popup_content = f"<strong>Iceberg ID:</strong> {iceberg}<br><strong>Width:</strong> {width} meters<br><strong>Height:</strong> {height} meters"
                
                # Create GeoJson with popup
                folium.GeoJson(
                    gdf.__geo_interface__,
                    name=iceberg,
                    style_function=lambda x, color=color: {"color": color, "weight": 1},
                    popup=folium.Popup(popup_content, max_width=300)  # Add popup
                ).add_to(m)
                
                # Zoom into iceberg centroid
                centroid = gdf.geometry.centroid.iloc[0]
                m.location = [centroid.y, centroid.x]
                m.zoom_start = 12
    else:
        site_path = os.path.join(shapefile_base_path, site_id, f"{early_date}-{later_date}")
        if os.path.exists(site_path):
            if plot_all:
                shapefiles = [f for f in os.listdir(site_path) if f.endswith(".shp")]
            else:
                shapefiles = selected_icebergs
                
            for iceberg in shapefiles:
                shp_path = os.path.join(site_path, iceberg)
                gdf = load_and_reproject_shapefile(shp_path)
                
                # Calculate width and height
                width, height = calculate_width_height(gdf)
                
                # Determine color based on date (blue for early_date, green for later_date)
                if early_date in iceberg:
                    color = "blue"
                elif later_date in iceberg:
                    color = "green"
                else:
                    color = "gray"  # Default to gray
                
                # Create popup with width and height
                popup_content = f"<strong>Iceberg ID:</strong> {iceberg}<br><strong>Width:</strong> {width} meters<br><strong>Height:</strong> {height} meters"
                
                # Create GeoJson with popup
                folium.GeoJson(
                    gdf.__geo_interface__,
                    name=iceberg,
                    style_function=lambda x, color=color: {"color": color, "weight": 1},
                    popup=folium.Popup(popup_content, max_width=300)  # Add popup
                ).add_to(m)
                
                # Zoom into iceberg centroid
                centroid = gdf.geometry.centroid.iloc[0]
                m.location = [centroid.y, centroid.x]
                m.zoom_start = 12
    
    return m

# Main app
try:

    # Load glacier site data
    glacier_sites = pd.read_csv(csv_file_path)
    
    # User inputs
    site_id = st.sidebar.selectbox("Select Glacier Site", glacier_sites['Glacier_ID'].unique())
    early_date = st.sidebar.text_input("Enter Early Date (YYYYMMDD)", "")
    later_date = st.sidebar.text_input("Enter Later Date (YYYYMMDD)", "")
    
    # List available shapefiles
    shapefile_dir = os.path.join(shapefile_base_path, site_id, f"{early_date}-{later_date}")
    shapefiles = [f for f in os.listdir(shapefile_dir) if f.endswith(".shp")] if os.path.exists(shapefile_dir) else []
    
    # Option to select all or specific shapefiles, or all icebergs from all files
    plot_option = st.sidebar.radio("Plot icebergs:", ("Plot selected date range", "Select specific icebergs", "Choose violence: Plot all icebergs from all files"))
    
    if plot_option == "Select specific icebergs":
        selected_icebergs = st.multiselect("Select Icebergs to View", shapefiles, default=shapefiles[:1])
        plot_all = False
        plot_all_files = False
    elif plot_option == "Plot all icebergs from all files":
        selected_icebergs = []
        plot_all = False
        plot_all_files = True
    else:
        selected_icebergs = shapefiles  # All shapefiles
        plot_all = True
        plot_all_files = False
    
    # Generate map
    if selected_icebergs or plot_all_files:
        map_object = create_interactive_map(glacier_sites, site_id, early_date, later_date, selected_icebergs, plot_all, plot_all_files)
        st_folium(map_object, width=800, height=600)
    else:
        st.write("")
    
except Exception as e:
    st.error(f"An error occurred: {e}")
