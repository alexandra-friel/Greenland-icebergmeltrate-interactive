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


import importlib.util
import sys
from pathlib import Path

#CUSTOMIZE FUN APP COLORS HERE: 
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

# Function to dynamically load a module from a given path
def load_module_from_path(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module

# Sidebar for navigation
page = st.sidebar.selectbox(
    "Select a Page",
    ["Home", "Iceberg Shapefile Viewer", "Statistics Dashboard", "Research Methods","Map of Iceberg Distributions","Acknowledgements"]
)

# Navigation logic
if page == "Home":
    home_path = "/workspaces/Greenland-icebergmeltrate-interactive/Home.py"
    if Path(home_path).exists():
        home = load_module_from_path("Home", home_path)
        # home.app()  # Uncomment to call the app() function in Home.py
    else:
        st.error(f"🚫 Could not find the file: {home_path}")

elif page == "Iceberg Shapefile Viewer":
    page1_path = "/workspaces/Greenland-icebergmeltrate-interactive/page1.py"
    if Path(page1_path).exists():
        page1 = load_module_from_path("page1", page1_path)
        # page1.app()  # Uncomment to call the app() function in page1.py
    else:
        st.error(f"🚫 Could not find the file: {page1_path}")

elif page == "Statistics Dashboard":
    page2_path = "/workspaces/Greenland-icebergmeltrate-interactive/page2.py"
    if Path(page2_path).exists():
        page2 = load_module_from_path("page2", page2_path)
        # page2.app()  # Uncomment to call the app() function in page2.py
    else:
        st.error(f"🚫 Could not find the file: {page2_path}")

elif page == "Research Methods":
    page3_path = "/workspaces/Greenland-icebergmeltrate-interactive/page3.py"
    if Path(page3_path).exists():
        page3 = load_module_from_path("page3", page3_path)
        # page3.app()  # Uncomment to call the app() function in page3.py
    else:
        st.error(f"🚫 Could not find the file: {page3_path}")

elif page == "Map of Iceberg Distributions":
    page4_path = "/workspaces/Greenland-icebergmeltrate-interactive/page4.py"
    if Path(page4_path).exists():
        page3 = load_module_from_path("page4", page4_path)
        # page3.app()  # Uncomment to call the app() function in page3.py
    else:
        st.error(f"🚫 Could not find the file: {page4_path}")
        
elif page == "Acknowledgements":
    page5_path = "/workspaces/Greenland-icebergmeltrate-interactive/page5.py"
    if Path(page5_path).exists():
        page3 = load_module_from_path("page4", page5_path)
        # page3.app()  # Uncomment to call the app() function in page3.py
    else:
        st.error(f"🚫 Could not find the file: {page5_path}")
