import pandas as pd
import numpy as np

# import geopandas as gpd
import plotly.express as px
import streamlit as st
import visualization_func as vz
import aux_func as aux


# initial config parameters of the web page
st.set_page_config(
    page_title="Brazilian electric matrix analysis",
    page_icon=":bar_chart:",
    layout="wide",
    initial_sidebar_state="expanded",
)

# # read procesed data
# csv_file_path = r"https://github.com/mmanoso/Brazilian-electric-matrix/blob/main/data/processed/transformed_data_app.pkl?raw=true"
# dfData = pd.read_pickle(csv_file_path)

# # read geojson data
# geojson_file_path_state = r"C:\Users\Mariano\Documents\aprendizaje-data-science\repositorio-brazilian-electric-matrix\Brazilian-electric-matrix\data\processed\all_states.geojson"
# dfGeoData = gpd.read_file(geojson_file_path_state)
aux.initialize_session_state_data()
# obtain parameters for filtering data
fuel_type = st.session_state.dfData["fuel_origin"].unique()
generator_type = st.session_state.dfData["generator_type"].unique()
status = st.session_state.dfData["status"].unique()
map_category = ["fuel_origin", "generator_type"]

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
    # par_status = st.selectbox("Status", options=status, index=0)
    # Clasification for points in map
    par_category = st.selectbox("Category", options=map_category, index=0)


# title of the page
st.header("Brazilian electric matrix - Historical Evolution")
# description text
st.write(
    f"Historical evolution of installed electric power clasified by {par_category}."
)
# display of historicar evolution graph
fig = vz.hist_line_plot(st.session_state.dfData, par_category, color_scale="Plotly")
st.plotly_chart(fig, use_container_width=True)
