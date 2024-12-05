# 🧊An Iceberg Catalog for Analysis of Greenland Environments: ICE-AGE

### How to run it on your own machine

1. Install the requirements

   ```
   $ pip install -r requirements.txt
   ```

2. Run the app

   ```
   $ streamlit run streamlit_app.py
   ```
3. Alternatively, use  the link!

   ```
   $ (link goes here when it's ready!)
   ```

Be sure to have a Github account when you access this application! 

This Streamlit app prioritizes ease of use,  featuring an intuitive interface for selecting and analyzing iceberg shapefiles. Users can effortlessly view key metadata (I'd like to eventually add these shapefiles on a map for spatial context) all within just a few clicks. To get started, the users will select a site name from a dropdown menu and manually enter pre-determined dates in the "Earlier Date" and "Later Date" slots. A link to all available date pairings ensures easy reference. Once the user inputs their desired location and dates, the iceberg shapefiles will be displayed.

The plots will automatically adjust the axis boundaries based on the largest iceberg, which ensures proper scaling for comparative analysis. The icebergs are color-coded by date, with orange representing the earlier date and green representing the later date. (I will add a legend)

The shapefiles are then divided into four groups based on area, simplifying the identification of patterns in shape and size. Each group is displayed in its dedicated subplot, with overlapping shapes displayed  in low opacity. This will hopefully expose the trends and variations across groups while preserving individual details. 

Please note: Prior to user input for site name and dates, there may be an error: "area_df is not defined" - This will be resolved once user input is complete. 



