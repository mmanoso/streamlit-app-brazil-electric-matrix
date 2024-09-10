import pandas as pd
import numpy as np
import geopandas as gpd
import plotly.express as px
import streamlit as st
import visualization_func as vf

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

# read geojson data
geojson_file_path_state = r"https://github.com/mmanoso/Brazilian-electric-matrix/blob/main/data/processed/all_states.geojson?raw=true"
dfGeoData = gpd.read_file(geojson_file_path_state)

# obtain parameters for filtering data
fuel_type = dfData["fuel_origin"].unique()
generator_type = dfData["generator_type"].unique()
status = dfData["status"].unique()
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
    #    "Generator Type", options=generator_type, default=generator_type
    # )
    # Status of the plant
    par_selec_status = st.selectbox("Status", options=status, index=0)
    # Clasification for points in map
    par_category = st.selectbox("Category", options=map_category, index=0)

# title of the page
st.header("Brazilian electric matrix - Home")

# map with location of power plants
fig = vf.loc_map_plot(
    df=dfData,
    geodf=dfGeoData,
    status=par_selec_status,
    category=par_category,
    color_scale="Pastel",
)
st.plotly_chart(fig, use_container_width=True)

# data for total operative, projected and construction electric power
c1, c2, c3 = st.columns(3)
with c1:
    operative_electric_power = (
        dfData.loc[dfData["status"] == "Operação", "electric_power_inst"].sum()
    ) / 1000
    st.metric(f"Total Installed Electric Power", f"{operative_electric_power:,.0f} MW")

with c2:
    proj_electric_power = (
        dfData.loc[
            dfData["status"] == "Construção não iniciada",
            "electric_power_inst",
        ].sum()
    ) / 1000
    st.metric(f"Total Projected Electric Power", f"{proj_electric_power:,.0f} MW")

with c3:
    constr_electric_power = (
        dfData.loc[dfData["status"] == "Construção", "electric_power_inst"].sum()
    ) / 1000
    st.metric(
        f"Total in Construction Electric Power", f"{constr_electric_power:,.0f} MW"
    )
