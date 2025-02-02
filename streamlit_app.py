import streamlit as st
import importlib.util
import sys
from pathlib import Path
import warnings

# This will suppress warnings on the front end of the application:
warnings.filterwarnings("ignore")

# This will allow you to customize the appearance of the front end:
# Google "Color Hex Picker" for all of the color codes! One should pop up right away.
st.markdown(
    """
    <style>
    .stApp { background-color: #2f3338; } 
    [data-testid="stSidebar"] { background-color: #082047; }
    .stTitle { color: #000000; }
    </style>
    """,
    unsafe_allow_html=True
)


# This function will dynamically load a module from a specified path.
def load_module_from_path(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module

# This is the sidebar for navigating to new pages:
page = st.sidebar.selectbox(
    "Page Navigation",
    [
        "Home", #Shows the main focus of the application
        "Iceberg Shapefile Viewer", #Loads and displays iceberg shapefiles, then divides plots into quartiles.
        "Statistics Dashboard", #Loads and displays iceberg melt information and associated statistics.
        "Research Methods", #Displays the methods used for data generation and work flow
        "Map of Iceberg Distributions", #Interactive map to see spatial orientation of icebergs
        "Field Work Experiences",  #Fun pictures from the field!
        "Acknowledgements" #Displays authors and award numbers.
    ]
)

# If/else logic for page navigation: 

if page == "Home":
    home_path = "/workspaces/Greenland-icebergmeltrate-interactive/Navigation-pages/Home.py"
    if Path(home_path).exists():
        home = load_module_from_path("Home", home_path)
        # home.app()  
    else:
        st.error(f"🚫 Could not find the file: {home_path}")

elif page == "Iceberg Shapefile Viewer":
    page1_path = "/workspaces/Greenland-icebergmeltrate-interactive/Navigation-pages/Iceberg-shapefile-viewer.py"
    if Path(page1_path).exists():
        page1 = load_module_from_path("page1", page1_path)
        # page1.app()  
    else:
        st.error(f"🚫 Could not find the file: {page1_path}")

elif page == "Statistics Dashboard":
    page2_path = "/workspaces/Greenland-icebergmeltrate-interactive/Navigation-pages/Statistics-dashboard.py"
    if Path(page2_path).exists():
        page2 = load_module_from_path("page2", page2_path)
        # page2.app()  
    else:
        st.error(f"🚫 Could not find the file: {page2_path}")

elif page == "Research Methods":
    page3_path = "/workspaces/Greenland-icebergmeltrate-interactive/Navigation-pages/Research-methods.py"
    if Path(page3_path).exists():
        page3 = load_module_from_path("page3", page3_path)
        # page3.app()  
    else:
        st.error(f"🚫 Could not find the file: {page3_path}")

elif page == "Map of Iceberg Distributions":
    page4_path = "/workspaces/Greenland-icebergmeltrate-interactive/Navigation-pages/Iceberg-spatial-distributions.py"
    if Path(page4_path).exists():
        page4 = load_module_from_path("page4", page4_path)
        # page4.app() 
    else:
        st.error(f"🚫 Could not find the file: {page4_path}")

elif page == "Field Work Experiences":
    page5_path = "/workspaces/Greenland-icebergmeltrate-interactive/Navigation-pages/Field-Work-images.py"
    if Path(page5_path).exists():
        page5 = load_module_from_path("page5", page5_path)
        #page5.app()  
    else:
        st.error(f"🚫 Could not find the file: {page5_path}")
