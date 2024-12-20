import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os
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

# Title and introductory information
st.title('📊 Iceberg Statistics Dashboard')
st.markdown('This page will allow you to......')
st.info('Click here for the [Fjord Abbreviation List & Paired Dates](https://docs.google.com/spreadsheets/d/1kCcKqf717kK3_Xx-GDe0f61jhlUpZ5n6BN1qtiw7S4w/edit?gid=0#gid=0)')

# Base directory where data is stored
base_path = "/workspaces/Greenland-icebergmeltrate-interactive/Melt-rates"

# Sidebar inputs
st.sidebar.header("Inputs")
site_name = st.sidebar.selectbox("Select Site Name:", ["KOG", "SEK", "ASG"])
early_date = st.sidebar.text_input("Enter Early Date (YYYYMMDD):", "")  # Example: 20170515
later_date = st.sidebar.text_input("Enter Later Date (YYYYMMDD):", "")  # Example: 20170611

# Sidebar images
st.sidebar.image("Iceberg-images/Ice-bridge-streamlit.png", caption="Surprising iceberg shapes drift in the coastal waters near Ilulissat, Greenland. Credit: Twila Moon, NSIDC")
st.sidebar.image("Iceberg-images/Icebergs-streamlit.png", caption="An iceberg drifts in the sea off the coast of Ilulissat, Greenland. Credit: Twila Moon, NSIDC")
st.sidebar.image("Iceberg-images/Sunset-icebergs-streamlit.png", caption="Icebergs crowd the waters along the northwestern Greenland coast. Credit: Twila Moon, NSIDC")

# Add placeholder for the GIF or animation
gif_placeholder = st.empty()

# Display the penguin smack GIF
gif_placeholder.markdown(
    """
    <div style="display: flex; justify-content: center;">
        <img src="https://media.giphy.com/media/jxETRYAi2KReel7pqy/giphy.gif" alt="penguin smack gif" width="500">
    </div>
    """,
    unsafe_allow_html=True
)

# Construct folder and file paths
if site_name and early_date and later_date:
    folder_path = os.path.join(base_path, site_name, f"{early_date}-{later_date}")
    csv_file_name = f"{site_name}_{early_date}-{later_date}_iceberg_meltinfo.csv"
    csv_file_path = os.path.join(folder_path, csv_file_name)

    # Check if file exists
    if os.path.exists(csv_file_path):
        # Clear the GIF once the data loads
        gif_placeholder.empty()

        st.success("🎉 CSV file found! 🎉")
        # Load the CSV file
        df = pd.read_csv(csv_file_path)
        st.write("### Iceberg Meltrate Information:")
        st.dataframe(df)

        # Drop unwanted columns
        unwanted_columns = ['X_i', 'Y_i', 'TimeSeparation', 'VerticalAdjustment_i', 'VerticalAdjustment_f', 'Density_i', 'Density_f']
        df = df.drop(columns=[col for col in unwanted_columns if col in df.columns])

        # Display the correlogram
        st.write("### Correlogram of Iceberg Features")
        fig, ax = plt.subplots(figsize=(10, 8))
        sns.heatmap(df.corr(), annot=True, fmt=".2f", cmap="coolwarm", ax=ax)
        st.pyplot(fig)

    else:
        # Clear the GIF if file not found, but show error
        gif_placeholder.empty()
        st.error("🚫 CSV file not found. Please check your inputs! 🚫")
else:
    st.warning("⚠️ Please provide all inputs: Site Name, Early Date, and Later Date.")
