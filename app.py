"""Displaying geospatial enrollment data."""

import os
import numpy as np
import pandas as pd
import pydeck as pdk
import streamlit as st

# SETTING PAGE CONFIG TO WIDE MODE AND ADDING A TITLE AND FAVICON
st.set_page_config(layout="wide", page_title="Where do the applications come from?", page_icon=":student:")

# LOAD DATA ONCE
@st.cache_resource
def load_data():
    """Load and validate the application data."""
    path = "data.csv"
    if not os.path.isfile(path):
        path = f"https://github.com/jacek-jonca/geo-apps/raw/main/{path}"

    try:
        data = pd.read_csv(
            path,
            names=["lon", "lat"],
            skiprows=1,
            usecols=[0, 1],
        ).dropna()
        if data.empty:
            st.error("Data file is empty. Please check the source.")
            st.stop()
    except Exception as e:
        st.error(f"Error loading data: {e}")
        st.stop()

    return data

# FUNCTION FOR MAPS
def render_map(data, lon, lat, zoom, title, population):
    """Render a map using PyDeck."""
    st.write(f"{title} {population}")
    st.pydeck_chart(
        pdk.Deck(
            map_style="mapbox://styles/mapbox/light-v9",
            initial_view_state=pdk.ViewState(
                longitude=lon,
                latitude=lat,
                zoom=zoom,
                max_zoom=16,
                pitch=45,
                bearing=0,
            ),
            layers=[
                pdk.Layer(
                    "HexagonLayer",
                    data=data,
                    get_position=["lon", "lat"],
                    radius=500,
                    elevation_scale=25,
                    elevation_range=[0, 2000],
                    auto_highlight=True,
                    pickable=True,
                    extruded=True,
                    coverage=1,
                ),
            ],
        )
    )

# CALCULATE MIDPOINT FOR GIVEN SET OF DATA
@st.cache_data
def calculate_midpoint(data):
    """Calculate the geographic midpoint."""
    return (np.average(data["lon"]), np.average(data["lat"]))

# STREAMLIT APP LAYOUT
data = load_data()

# Validate if data has enough records
if data.shape[0] < 2:
    st.error("Insufficient data for visualization. Please check the source file.")
    st.stop()

# LAYING OUT THE TOP SECTION OF THE APP
st.title("Enrollment Sources Data")
st.markdown("## Visualizing enrollments")

# DEFINE CITY LOCATIONS
locations = {
    "All Texas": [-99.17065, 31.391533],
    "Houston": [-95.3701, 29.7601],
    "Dallas": [-96.9209, 32.7079],
    "Austin": [-97.7405, 30.2747],
    "San Antonio": [-98.4911, 29.4243],
    "Killeen": [-97.7278, 31.1171],
}

# SETTING GEOGRAPHIC MIDPOINT
midpoint = calculate_midpoint(data)

# LAYING OUT THE STREAMLIT APP WITH SPECIFIC ROW ARRANGEMENT
# Row 1: Full-width map for "All Texas"
render_map(data, midpoint[0], midpoint[1], 7, "Geographic Midpoint of the Data", " ")

# Row 2: Full-width map for "Houston"
render_map(data, locations["Houston"][0], locations["Houston"][1], 9, "Houston, ", "population: 7.5 million")

# Row 3: Four equal-width maps for "Dallas," "Austin,", "San Antonio", and "Killeen"
row3_col1, row3_col2, row3_col3, row3_col4 = st.columns(4)

with row3_col1:
    render_map(data, locations["Dallas"][0], locations["Dallas"][1], 9, "Dallas, ", "population: 8.1 million")

with row3_col2:
    render_map(data, locations["San Antonio"][0], locations["San Antonio"][1], 9, "San Antonio, ", "population: 2.7 million")

with row3_col3:
    render_map(data, locations["Austin"][0], locations["Austin"][1], 9, "Austin, ", "population: 2.5 million")

with row3_col4:
    render_map(data, locations["Killeen"][0], locations["Killeen"][1], 9, "Killeen, ", "population: 0.5 million")