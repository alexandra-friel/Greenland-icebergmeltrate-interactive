import streamlit as st
import warnings

# CUSTOMIZE FUN APP COLORS HERE:
st.markdown(
    """
    <style>
    /* Main page background color */
    .stApp {
        background-color: #1a1a1a;  /* Dark background */
    }
    /* Sidebar background color */
    [data-testid="stSidebar"] {
        background-color: #333333;  /* Darker sidebar */
    }
    /* Title text color */
    .stTitle {
        color: white;  /* White title text */
        font-size: 2rem;
        font-weight: bold;
    }
    /* Info box styling */
    .stInfo {
        background-color: #444444;  /* Dark gray info box */
        color: white;
    }
    /* Card styling */
    .card {
        background-color: #2c2c2c;  /* Dark card background */
        padding: 20px;
        border-radius: 8px;
        box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.3);
        margin-bottom: 20px;
        color: white;  /* White text in cards */
    }
    /* Text and links styling */
    .stMarkdown a {
        color: #4a90e2;  /* Light blue link color */
        text-decoration: none;
        font-weight: bold;
    }
    .stMarkdown a:hover {
        text-decoration: underline;
    }
    /* Image styling */
    .stImage {
        border-radius: 10px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

warnings.filterwarnings("ignore")

# Titles and content
st.title("🥳 Acknowledgements:")
st.info("Project funding via NSF Arctic Natural Sciences awards #2052561, #2052549, #205255")
st.markdown("""
            <div class="card">
                <ul>
                    <li><strong>Authors:</strong> Twila A. Moon, Dustin Carroll, Ellyn Enderlin, Aman KC, Alexandra Friel</li>
                    <li><strong>Institutions:</strong> Boise State University, University of Colorado Boulder, San Jose State University, National Snow and Ice Data Center, Cooperative Institute for Research in Environmental Sciences, & Jet Propulsion Laboratory California Institute of Technology</li>
                    <li><strong>Data Generation:</strong> Alexandra Friel, Isabella Welk, Alex Iturriria, Madelyn Woods</li>
                    <li><strong>Data Visualization & Streamlit Application Development:</strong> Alexandra Friel</li>
                </ul>
            </div>
""", unsafe_allow_html=True)

st.title("🔮 The Future of ICE-AGE:")
st.markdown("""
            <div class="card">
                ICE-AGE is designed as a database that can grow and evolve. The full code and workflow for ICE-AGE will be publicly accessible. ICE-AGE is meant as a community resource to reduce the idea-to-research timeline for iceberg-focused research. Within our team, ICE-AGE will inform ongoing work focused on improved freshwater flux estimates for Greenland and improved representation of iceberg-derived freshwater flux in models using DEM-differenced melt rates and an iceberg melt model.
            </div>
""", unsafe_allow_html=True)

# Sidebar with images aligned side by side
col1, col2 = st.sidebar.columns(2)

# Image for NSIDC on the left column
with col1:
    st.image("/workspaces/Greenland-icebergmeltrate-interactive/Iceberg-images/NSIDC-Streamlit.png", caption="NSIDC Banner", use_container_width=True, width=240)

# Image for NSF on the right column
with col2:
    st.image("/workspaces/Greenland-icebergmeltrate-interactive/Iceberg-images/NSF-streamlit.png", caption="NSF Banner", use_container_width=True, width=250)

# Existing sidebar images
st.sidebar.image("/workspaces/Greenland-icebergmeltrate-interactive/Iceberg-images/Institutions-streamlit.png")
st.sidebar.image("Iceberg-images/Scenic-glacier-streamlit.png", caption="Tundra ponds form along the coast near Ilulissat, Greenland, while icebergs are visible along the horizon. Credit: Twila Moon, NSIDC")
st.sidebar.image("Iceberg-images/Chilly-iceberg-streamlit.png", caption="Credit: Twila Moon, NSIDC")

# Links section
st.markdown("<h3>If you liked this ICE-AGE application, you may also be interested in: </h3>", unsafe_allow_html=True)
st.markdown("[ICEBERGER: Interactive Tool for Iceberg Research](https://joshdata.me/iceberger.html)")
st.markdown("[Zenodo Record - ICE-AGE Data](https://zenodo.org/records/8007035)")












