import pandas as pd
import numpy as np
import geopandas as gpd
import plotly.express as px
import streamlit as st
import visualization_func as vf
import aux_func as aux


# function to ensure loading the data
def ensure_data_loaded():
    if not st.session_state.get("dfData_loaded", False):
        aux.initialize_session_state_data()
    return st.session_state.dfData


def ensure_geedata_loaded():
    if not st.session_state.get("dfGeoData_loaded", False):
        aux.initialize_session_state_geodata()
    return st.session_state.dfGeoData


# define function for kpi of electric power
def render_kpi_electric_power() -> None:
    """Create KPI for Installed, Porjected and In construction electric power"""

    # data for total operative, projected and construction electric power
    c1, c2, c3 = st.columns(3)
    with c1:
        operative_electric_power = (
            st.session_state.dfData.loc[
                st.session_state.dfData["status"] == "Operação", "electric_power_inst"
            ].sum()
        ) / 1000
        st.metric(
            f"Total Installed Electric Power", f"{operative_electric_power:,.0f} MW"
        )

    with c2:
        proj_electric_power = (
            st.session_state.dfData.loc[
                st.session_state.dfData["status"] == "Construção não iniciada",
                "electric_power_inst",
            ].sum()
        ) / 1000
        st.metric(f"Total Projected Electric Power", f"{proj_electric_power:,.0f} MW")

    with c3:
        constr_electric_power = (
            st.session_state.dfData.loc[
                st.session_state.dfData["status"] == "Construção", "electric_power_inst"
            ].sum()
        ) / 1000
        st.metric(
            f"Total in Construction Electric Power", f"{constr_electric_power:,.0f} MW"
        )


def main() -> None:
    """Main function to run the streamlit app in Main Page"""

    # page configuration
    st.set_page_config(
        page_title="Brazilian electric matrix analysis",
        page_icon=":bar_chart:",
        layout="wide",
        initial_sidebar_state="expanded",
    )

    # initialize data of original dataframe and geodataframe
    # aux.initialize_session_state_data()
    # aux.initialize_session_state_geodata()
    ensure_data_loaded()
    ensure_geedata_loaded()
    aux.initialize_session_state_variables()

    # render sidebar with pages naviation
    aux.render_sidebar()

    # add filters to sidebar
    with st.sidebar:
        # Status of the plant
        par_selec_status = st.selectbox(
            "Status", options=st.session_state.status, index=0
        )
        # Clasification for points in map
        par_category = st.selectbox(
            "Category", options=st.session_state.map_category, index=0
        )
    # title of the page
    st.header("Brazilian electric matrix - Home")

    # map with location of power plants
    fig = vf.loc_map_plot(
        df=st.session_state.dfData,
        geodf=st.session_state.dfGeoData,
        status=par_selec_status,
        category=par_category,
        color_scale="Pastel",
    )
    st.plotly_chart(fig, use_container_width=True)

    # render display of kpi for electric power
    render_kpi_electric_power()


if __name__ == "__main__":
    main()
