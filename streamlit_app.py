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
        background-color: #708899;
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
        st.title("Welcome to the Main Page")
        st.write("This is the main landing page. Use the sidebar to navigate.")
    elif page == "Page 1":
        # Load and execute external page1.py
        page1_path = "/workspaces/rotate-icebergs/page1.py"
        if Path(page1_path).exists():
            page1 = load_module_from_path("page1", page1_path)
            page1.app()  # Call the app() function in page1.py
        else:
            st.error(f"🚫 Could not find the file: {page1_path}")
    elif page == "Page 2":
        # Load and execute external page2.py
        page2_path = "/workspaces/rotate-icebergs/page2.py"
        if Path(page2_path).exists():
            page2 = load_module_from_path("page2", page2_path)
            page2.app()  # Call the app() function in page2.py
        else:
            st.error(f"🚫 Could not find the file: {page2_path}")

if __name__ == "__main__":
    main()


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
