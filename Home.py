import streamlit as st

# Custom CSS to change the background and text color of the info box
st.markdown(
    """
    <style>
    .custom-info-box {
        background-color: #7d6ceb; 
        color: #000000; /* Black text */
        padding: 1rem;
        border-radius: 1rem;
        border: 1px solid #b26ceb; 
    }
    </style>
    <div class="custom-info-box">
        🚨 ICE-AGE is under development, please hang tight if there is missing data! 🚨 
    </div>
    """,
    unsafe_allow_html=True
)

st.title("🧊ICE-AGE Innovation: A new Iceberg Catalog Empowering Analysis of Greenland Environments")
st.markdown("The new ICE-AGE data catalog will provide an easy access point for identifying icebergs, associated metrics, and usable data and imagery for jump-starting your iceberg research.")
st.markdown("<h3>How was ICE-AGE created?</h3>", unsafe_allow_html=True)
st.markdown("Satellite imagery analysis & DEM differencing:")
st.image("DEM-differencing-Streamlit.png")
st.info("Example of high- resolution iceberg elevation observations for melt rate estimates. Method: Enderlin & Hamilton ( 2014).")
st.markdown("ICE-AGE will initially reflect results from very high-resolution satellite imagery for 2011-2023. The processing pipeline can be applied to a variety of imagery types, including ArcticDEM time-stamped DEMs. Code development is public via GitHub and current code version available at https://doi.org/10.5281/zenodo.8011424")
st.markdown("")
st.markdown("Automated iceberg detection for distributions:")
st.image("DrJukes-Streamlit.png")
st.info("Learn more about iceberg and ice mélange fragmentation theory within Enderlin, E., A. Friel, J. Liu, & M. Kopera, 2023. Greenland ice mélange fragmentation theory curve parameters from digital elevation models (2011-2020). Arctic Data Center. doi:10.18739/A2SX64B7D.")
st.markdown("")

st.markdown("<h3>How to access ICE-AGE: </h3>", unsafe_allow_html=True)
st.markdown("ICE-AGE data will be archived at the Arctic Data Center. Code will be available via GitHub, released via Zenodo, and designed to allow for future database growth and automated figure generation.")
st.markdown("")
st.title("Contents of ICE-AGE application:")
#st.image("Iceberg-metrics-streamlit.png", width = 300)
#st.info("This diagram is not a realistic iceberg shape! To explore iceberg equilibrium in the water, check out Iceberger! https://joshdata.me/iceberger.html")

st.markdown("<h3>📈Individual Iceberg Metrics:</h3>", unsafe_allow_html=True)

st.markdown("""
            - Iceberg location and the repeat imagery metadata needed to identify and study that iceberg.
            - Open access code will provide a pathway to connect from shapefiles to other ICE-AGE metrics
            - Shapefiles for iceberg map-view imaging
            - Iceberg width, length, height, volume, and draft. 
            - Iceberg subaerial area and submerged data. 
""")

st.markdown("<h3>⏱️Change over time Metrics:</h3>", unsafe_allow_html=True)
st.markdown("""
            - Volume change rate
            - Elevation change rate
""")
st.markdown("<h3>🏞️Regional Iceberg Metrics:</h3>", unsafe_allow_html=True)
st.markdown("""
            - Iceberg size distributions for selection of times and locations. 


""")

st.sidebar.image("aerial-shot-streamlit.png", caption = "Low-angled sunlight illuminates Antarctica’s Matusevich Glacier in this image from September 6, 2010. The image was acquired by the Advanced Land Imager (ALI) on NASA’s Earth Observing-1 (EO-1) satellite, and it shows a deeply crevassed glacier breaking apart amid ocean waves. Credit: NASA")
st.sidebar.image("aerial-iceborgs.png", caption = "Aerial view of icebergs in the sea ice near Qaanaaq, Greenland. Icebergs form when chunks of ice calve, or break off, from glaciers, ice shelves, or a larger iceberg. The North Atlantic and the cold waters surrounding Antarctica are home to most of the icebergs on Earth.Credit: Shari Fox, NSIDC")