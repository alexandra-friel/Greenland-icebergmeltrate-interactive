import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os
import warnings
import graphviz


import importlib.util
import sys
from pathlib import Path

#CUSTOMIZE FUN APP COLORS HERE: 
st.markdown(
    """
    <style>
    /* Main page background color */
    .stApp {
        background-color: #5c5f61;
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

def main():
    # Sidebar for navigation
    st.sidebar.title("Navigation")
    page = st.sidebar.radio("Go to", ["Home", "Page 1", "Page 2"])



    # Navigation logic
    if page == "Home":
        st.title("🧊ICE-AGE Innovation: a new Iceberg Catalog Empowering Analysis of Greenland Environments❄️")
    elif page == "Page 1":
        # Load and execute external page1.py
        page1_path = ("/workspaces/Greenland-icebergmeltrate-interactive/page1.py")
        if Path(page1_path).exists():
            page1 = load_module_from_path("page1", page1_path)
            #page1.app()  # Call the app() function in page1.py
        else:
            st.error(f"🚫 Could not find the file: {page1_path}")
    elif page == "Page 2":
        # Load and execute external page2.py
        page2_path = ("/workspaces/Greenland-icebergmeltrate-interactive/page2.py")
        if Path(page2_path).exists():
            page2 = load_module_from_path("page2", page2_path)
           # page2.app()  # Call the app() function in page2.py
        else:
            st.error(f"🚫 Could not find the file: {page2_path}")

if __name__ == "__main__":
    main()

st.sidebar.image("aerial-shot-streamlit.png", caption = "Low-angled sunlight illuminates Antarctica’s Matusevich Glacier in this image from September 6, 2010. The image was acquired by the Advanced Land Imager (ALI) on NASA’s Earth Observing-1 (EO-1) satellite, and it shows a deeply crevassed glacier breaking apart amid ocean waves. Credit: NASA")
st.sidebar.image("aerial-iceborgs.png", caption = "Aerial view of icebergs in the sea ice near Qaanaaq, Greenland. Icebergs form when chunks of ice calve, or break off, from glaciers, ice shelves, or a larger iceberg. The North Atlantic and the cold waters surrounding Antarctica are home to most of the icebergs on Earth.Credit: Shari Fox, NSIDC")
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
st.markdown("\n\n")

st.title("How ICE-AGE was created: ")
st.markdown("""
            - ICE-AGE will initially reflect results from very high-resolution satellite imagery for 2011-2023. The processing pipeline can be applied to a variety of imagery types, including ArcticDEM time-stamped DEMs.
""")
st.markdown("\n\n")

st.title("🔮The Future of ICE-AGE: ")
st.markdown("""
            - ICE-AGE is designed as a database that can grow and evolve. The full code and workflow for ICE-AGE will be publicly accessible. ICE-AGE is meant as a community resource to reduce the idea-to-research timeline for iceberg-focused research. Within our team, ICE-AGE will inform ongoing work focused on improved freshwater flux estimates for Greenland and improved representation of iceberg-derived freshwater flux in models using DEM-differenced melt rates and an iceberg melt model.
""")

st.markdown("\n\n")
st.title("📈Individual Iceberg Metrics: ")
st.markdown("""
            - Open access code will provide a pathway to connect from shapefiles to other ICE-AGE metrics
            - Shapefiles for iceberg map-view imaging
            - Iceberg width, length, height, volume, and draft. 
            - Iceberg subaerial area and submerged data. 
""")
st.markdown("\n\n")
st.title("⌛Change over Time Metrics: ")
st.markdown("""
            - Volume change rate
            - Elevation change rate
""")
st.markdown("\n\n")
st.title("🏞️Regional Iceberg Metrics: ")
st.markdown("""
            - Iceberg size distributions for selection of times and locations. 




""")
st.markdown("\n\n")
st.title("🥳Acknowledgements:")
st.markdown("""
            - Authors: Twila A. Moon, Dustin Carroll, Alexandra Friel, Ellyn Enderlin, Aman KC
            - Institutions: Boise State Univeristy, University of Colorado Boulder, National Snow and Ice Data Center, Cooperative Institute for Research in Environmental Sciences, San Jose State University
            - Data Generation: Alexandra Friel, Isabella Welk, Alex Iturriria, Madelyn Woods
            - Data Visualization & Streamlit Application Development: Alexandra Friel
""")
