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
column_names = ["fuel_origin", "fuel_type", "fuel_type_name", "generator_type"]

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
    # fuel origin
    par_multi_fuel_origin = st.multiselect(
        "Fuel Origin", options=fuel_origin, default=None
    )
    # Fuel type
    par_multi_fuel_type = st.multiselect("Fuel Type", options=fuel_type, default=None)
    # fuel type name
    par_multi_fuel_type_name = st.multiselect(
        "Fuel Type Name", options=fuel_type_name, default=None
    )
    # Generator type
    par_multi_generator_type = st.multiselect(
        "Generator Type", options=generator_type, default=None
    )
    # states
    par_multi_states = st.multiselect("States", options=states, default=None)
    # Status of the plant
    # par_status = st.selectbox("Status", options=status, index=0)
    # Clasification for points in map
    # par_category = st.selectbox("Category", options=column_names, index=0)

# define variables becouse the first use dont define them


# title of the page
st.header("Brazilian electric matrix - Electric Matrix")

par_multi_status = st.multiselect("Status", options=status, default=status)
# par_selec_status = list(st.selectbox("Status", options=status, index=0))
par_multi_category = st.multiselect(
    "Category", options=column_names, default=column_names
)
par_selec_category = st.selectbox("Graph Type", options=column_names, index=0)
# graphs title
st.subheader(f"Electric Power by {par_selec_category}")
# apply filters to data
df_filtered = aux.apply_filters_to_df(
    df=dfData,
    status=par_multi_status,
    states=par_multi_states,
    fuel_origin=par_multi_fuel_origin,
    fuel_type=par_multi_fuel_type,
    fuel_type_name=par_multi_fuel_type_name,
    generator_type=par_multi_generator_type,
)

df_grouped = aux.groupby_func_to_df(df_filtered, par_multi_category)

# manage colors for graphs
color_dict = vz.generate_color_dict_plotly(
    categories=dfData[par_selec_category].unique(), colormap="Pastel"
)
# graphs
c1, c2 = st.columns(2)
with c1:
    fig = vz.bar_plot_status_category(
        df_grouped, category=par_selec_category, color_dict=color_dict
    )
    st.plotly_chart(fig, use_container_width=True)

with c2:
    fig = vz.pie_plot_status_category(
        df_grouped, category=par_selec_category, color_dict=color_dict
    )
    st.plotly_chart(fig, use_container_width=True)

# display table
st.subheader("Table for total Electric Power")
st.table(df_grouped)
