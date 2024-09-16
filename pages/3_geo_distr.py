import pandas as pd
import numpy as np
import geopandas as gpd
import plotly.express as px
import streamlit as st
import visualization_func as vz
import aux_func as aux


def render_map_graphs(par_status, par_category) -> None:
    """Create Choropleth map and points map"""
    c1, c2 = st.columns([0.5, 0.5])

    with c1:
        # st.subheader(f"Choropleth map by {par_status}")
        fig = vz.choropleth_mapbox_ele_pow(
            st.session_state.dfData, st.session_state.dfGeoData, par_status, "cividis"
        )
        st.plotly_chart(fig, use_container_width=True)

    with c2:
        # st.subheader(f"Locations map by {par_status} and {par_category}")
        fig = vz.loc_map_plot(
            st.session_state.dfData,
            st.session_state.dfGeoData,
            par_status,
            par_category,
            "Plotly",
        )
        st.plotly_chart(fig, use_container_width=True)


def main() -> None:
    """Main function to run the streamlit app in Page 3 Geographical Distribution"""
    # page configuration
    st.set_page_config(
        page_title="Brazilian electric matrix analysis",
        page_icon=":bar_chart:",
        layout="wide",
        initial_sidebar_state="expanded",
    )

    # initialize data, geodata and variables
    aux.initialize_session_state_data()
    aux.initialize_session_state_geodata()
    aux.initialize_session_state_variables()

    # render sidebar navigation across pages
    aux.render_sidebar()

    # add filters to sidebar
    with st.sidebar:

        # Status of the plant
        par_status = st.selectbox("Status", options=st.session_state.status, index=0)
        # Clasification for points in map
        par_category = st.selectbox(
            "Category", options=st.session_state.map_category, index=0
        )

    # title of the page
    st.header("Brazilian electric matrix - Geo Spacial Distribution")
    st.write(
        f"Brazilian map with electric power distribution by {par_status} and location of electric generators by {par_category}."
    )

    # render maps to plot
    render_map_graphs(par_category=par_category, par_status=par_status)


if __name__ == "__main__":
    main()
