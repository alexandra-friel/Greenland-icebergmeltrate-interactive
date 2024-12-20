import streamlit as st
import warnings

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

st.title("🥳Acknowledgements:")
st.markdown("""
            - Authors: Twila A. Moon, Dustin Carroll, Ellyn Enderlin, Aman KC, Alexandra Friel
            - Institutions: Boise State Univeristy, University of Colorado Boulder, San Jose State University, National Snow and Ice Data Center, Cooperative Institute for Research in Environmental Sciences, & Jet Propulsion Laboratory California Institute of Technology
            - Data Generation: Alexandra Friel, Isabella Welk, Alex Iturriria, Madelyn Woods
            - Data Visualization & Streamlit Application Development: Alexandra Friel
""")


st.title("🔮The Future of ICE-AGE: ")
st.markdown("""
            - ICE-AGE is designed as a database that can grow and evolve. The full code and workflow for ICE-AGE will be publicly accessible. ICE-AGE is meant as a community resource to reduce the idea-to-research timeline for iceberg-focused research. Within our team, ICE-AGE will inform ongoing work focused on improved freshwater flux estimates for Greenland and improved representation of iceberg-derived freshwater flux in models using DEM-differenced melt rates and an iceberg melt model.
""")



st.sidebar.image("Iceberg-images/Scenic-glacier-streamlit.png", caption = "Tundra ponds form along the coast near Ilulissat, Greenland, while icebergs are visible along the horizon. Credit: Twila Moon, NSIDC")
st.sidebar.image("Iceberg-images/Chilly-iceberg-streamlit.png", caption = "Credit: Twila Moon, NSIDC")


st.markdown("<h3>If you liked this ICE-AGE application, you may also be interested in: </h3>", unsafe_allow_html=True)
st.markdown("https://joshdata.me/iceberger.html")
st.markdown("https://zenodo.org/records/8007035")
