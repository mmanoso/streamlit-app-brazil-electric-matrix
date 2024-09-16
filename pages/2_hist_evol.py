import pandas as pd
import numpy as np

# import geopandas as gpd
import plotly.express as px
import streamlit as st
import visualization_func as vz
import aux_func as aux


def main() -> None:
    """Main function to run the streamlit app in Page 2 Historical Evolution"""
    # initial config parameters of the web page
    st.set_page_config(
        page_title="Brazilian electric matrix analysis",
        page_icon=":bar_chart:",
        layout="wide",
        initial_sidebar_state="expanded",
    )
    # initialize session state data and variables
    aux.initialize_session_state_data()
    aux.initialize_session_state_variables()

    # render sidebar with navigation across pages
    aux.render_sidebar()

    # add filter in sidebar
    with st.sidebar:
        # Clasification
        par_category = st.selectbox(
            "Category", options=st.session_state.map_category, index=0
        )

    # title of the page
    st.header("Brazilian electric matrix - Historical Evolution")

    # description text
    st.write(
        f"Historical evolution of installed electric power clasified by {par_category}."
    )

    # display of historicar evolution graph
    fig = vz.hist_line_plot(st.session_state.dfData, par_category, color_scale="Plotly")
    st.plotly_chart(fig, use_container_width=True)


if __name__ == "__main__":
    main()
