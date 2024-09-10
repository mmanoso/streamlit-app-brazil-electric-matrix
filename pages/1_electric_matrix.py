import pandas as pd
import numpy as np

# import geopandas as gpd
import plotly.express as px
import streamlit as st
import visualization_func as vz

# initial config parameters of the web page
st.set_page_config(
    page_title="Brazilian electric matrix analysis",
    page_icon=":bar_chart:",
    layout="wide",
    initial_sidebar_state="expanded",
)

# read procesed data
csv_file_path = r"https://github.com/mmanoso/Brazilian-electric-matrix/blob/main/data/processed/transformed_data_app.pkl?raw=true"
dfData = pd.read_pickle(csv_file_path)

# # read geojson data
# geojson_file_path_state = r"C:\Users\Mariano\Documents\aprendizaje-data-science\repositorio-brazilian-electric-matrix\Brazilian-electric-matrix\data\processed\all_states.geojson"
# dfGeoData = gpd.read_file(geojson_file_path_state)

# obtain unique values for parameters for filtering data
fuel_origin = dfData["fuel_origin"].unique()
fuel_type = dfData["fuel_type"].unique()
fuel_type_name = dfData["fuel_type_name"].unique()
generator_type = dfData["generator_type"].unique()
states = dfData["states"].unique()
status = dfData["status"].unique()
category_filter = ["fuel_origin", "fuel_type", "fuel_type_name", "generator_type"]

# configure the sidebar
with st.sidebar:
    # pages
    st.page_link("main_page.py", label="Home")
    st.page_link("pages/1_electric_matrix.py", label="Electric Matrix")
    st.page_link("pages/2_hist_evol.py", label="Historical Evolution")
    st.page_link("pages/3_geo_distr.py", label="Geographic Distribution")

st.sidebar.divider()

with st.sidebar:
    # Filters
    # Fuel type
    # par_fuel_type = st.multiselect("Fuel Type", options=fuel_type, default=fuel_type)
    # Generator type
    # par_generator_type = st.multiselect(
    #     "Generator Type", options=generator_type, default=generator_type
    # )
    # Status of the plant
    par_status = st.selectbox("Status", options=status, index=0)
    # Clasification for points in map
    par_category = st.selectbox("Category", options=category_filter, index=0)


# title of the page
st.header("Brazilian electric matrix - Electric Matrix")
st.subheader(f"Electric Power by {par_status} and by {par_category}")

c1, c2 = st.columns(2)
with c1:
    fig = vz.bar_plot_status_category(dfData, par_status, par_category, "Pastel")
    st.plotly_chart(fig, use_container_width=True)

with c2:
    fig = vz.pie_plot_status_category(dfData, par_status, par_category, "Pastel")
    st.plotly_chart(fig, use_container_width=True)

# display table
st.subheader("Table for total Electric Power")
display_table = (
    dfData[dfData["status"] == par_status]
    .groupby(["fuel_origin", "generator_type", "fuel_type"])
    .agg({"electric_power_inst": "sum"})
).reset_index()
st.table(display_table)
