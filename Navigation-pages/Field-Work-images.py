import streamlit as st
import warnings

# CUSTOMIZE FUN APP COLORS HERE:
st.markdown(
    """
    <style>
    /* Main page background color */
    .stApp {
        background-color: #1a1a1a;
    }
    /* Sidebar background color */
    [data-testid="stSidebar"] {
        background-color: #333333;
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