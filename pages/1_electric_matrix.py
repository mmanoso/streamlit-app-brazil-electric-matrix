import pandas as pd
import numpy as np
import plotly.express as px
import streamlit as st
from typing import List, Dict, Any
import visualization_func as vz
import aux_func as aux

# import file paths and constants
import config


# initialize session state variables
def initialize_session_state() -> None:
    """Initialize session state variables"""
    # data
    if "dfData" not in st.session_state:
        try:
            st.session_state.dfData = pd.read_pickle(config.csv_file_path)
        except Exception as e:
            st.error(f"Error loading data: {str(e)}")
            st.stop()

    # filters
    if "filters" not in st.session_state:
        st.session_state.filters = {
            "status": [],
            "fuel_origin": [],
            "fuel_type": [],
            "fuel_type_name": [],
            "generator_type": [],
            "states": [],
        }

    # filtered dataframe
    if "df_filtered" not in st.session_state:
        st.session_state.df_filtered = st.session_state.dfData

    # column names selection
    if "column_names_selec" not in st.session_state:
        st.session_state.column_names_selec = config.column_names_all

    # las valid column names selection
    if "column_names_last_selec" not in st.session_state:
        st.session_state.column_names_last_selec = config.column_names_all


# define function for sidebar navigation and filters
def render_sidebar() -> None:
    """Render the sidebar with navigations across pages and filters"""
    # configure the sidebar
    with st.sidebar:
        st.write("Navigation pages:")
        # pages
        st.page_link("main_page.py", label="Home")
        st.page_link("pages/1_electric_matrix.py", label="Electric Matrix")
        st.page_link("pages/2_hist_evol.py", label="Historical Evolution")
        st.page_link("pages/3_geo_distr.py", label="Geographic Distribution")

    st.sidebar.divider()

    with st.sidebar:
        # display filters to select
        st.write("Select the filters:")
        for filter_name in st.session_state.filters.keys():
            options = aux.get_filtered_options(
                st.session_state.dfData,
                filter_name,
                {k: v for k, v in st.session_state.filters.items() if k != filter_name},
            )
            st.session_state.filters[filter_name] = st.multiselect(
                f"Select {filter_name}",
                options=options,
                default=st.session_state.filters[filter_name],
            )

        # button to click to apply selected filters
        if st.button("Apply Filters"):
            st.session_state.df_filtered = aux.apply_filters_to_df(
                st.session_state.dfData,
                status=st.session_state.filters["status"],
                states=st.session_state.filters["states"],
                fuel_type=st.session_state.filters["fuel_type"],
                fuel_origin=st.session_state.filters["fuel_origin"],
                generator_type=st.session_state.filters["generator_type"],
                fuel_type_name=st.session_state.filters["fuel_type_name"],
            )


def apply_filters() -> None:
    """Apply selected filters to the dataframe"""
    try:
        st.session_state.df_filtered = aux.apply_filters_to_df(
            st.session_state.dfData, **st.session_state.filters
        )
    except Exception as e:
        st.error(f"Error applying filters: {str(e)}")


# function for render the main content of the page
def render_main_content() -> None:
    """Render the main content of the page"""
    # title of the page
    st.header("Brazilian electric matrix - Electric Matrix")

    # select filters to group and graph
    par_multi_category = st.multiselect(
        "Select columns to display in table:",
        options=config.column_names_all,
        default=st.session_state.column_names_selec,
        key="column_selector",
        on_change=update_column,
        args=(st.session_state.column_selector,),
    )

    par_selec_category = st.selectbox(
        "Select table column to graph:",
        options=st.session_state.column_names_selec,
        index=0,
    )
    # graphs title
    st.subheader(f"Electric Power by {par_selec_category}")

    # group dataframe acording to all filters
    df_grouped = aux.groupby_func_to_df(
        st.session_state.df_filtered, st.session_state.columns_names_selec
    )
    # apply function to visualize the graphs
    render_visualization()
    # apply function to visualize the table
    render_table()


def render_visualization(df_grouped: pd.Dataframe, category: str) -> None:
    """Render the graphs based on the grouped data"""
    # manage the color dictionary for the data
    color_dict = vz.generate_color_dict_plotly(
        categories=st.session_state.dfData[category].unique(),
        colormap="Pastel",
    )

    c1, c2 = st.columns(2)
    with c1:
        fig = vz.pie_plot_status_category(df_grouped, category, color_dict)
        st.plotly_chart(fig, use_container_width=True)
    with c2:
        fig = vz.bar_plot_status_category(df_grouped, category, color_dict)
        st.plotly_chart(fig, use_container_width=True)


def render_table(df_grouped: pd.Dataframe) -> None:
    """Render the table (dataframe) based on the grouped data"""
    st.subheader("Table for total Electric Power")
    st.table(df_grouped)


# function for forcing at least 1 option in a filter
def update_column(par_multi_category):
    """Update the selected columns and maintaining the last valid selection."""
    st.session_state.column_names_selec, st.session_state.column_names_last_selec = (
        aux.ensure_last_selection(
            par_multi_category, st.session_state.column_names_last_selec
        )
    )


def main() -> None:
    """Main function to run the streamlit app in Page 1 Electric Matrix"""
    # initial config parameters of the web page
    st.set_page_config(
        page_title="Brazilian electric matrix analysis",
        page_icon=":bar_chart:",
        layout="wide",
        initial_sidebar_state="expanded",
    )

    initialize_session_state()
    render_sidebar()
    render_main_content()
    # # initialize session state for orginal dataframe
    # if "dfData" not in st.session_state:
    #     # read procesed data
    #     csv_file_path = r"https://github.com/mmanoso/Brazilian-electric-matrix/blob/main/data/processed/transformed_data_app.pkl?raw=true"
    #     st.session_state.dfData = pd.read_pickle(csv_file_path)

    # # initialize filters in session state for dynamic filters
    # if "filters" not in st.session_state:
    #     st.session_state.filters = {
    #         "status": [],
    #         "fuel_origin": [],
    #         "fuel_type": [],
    #         "fuel_type_name": [],
    #         "generator_type": [],
    #         "states": [],
    #     }
    # # initialize dataframe in session state for dynamic filtering
    # if "df_filtered" not in st.session_state:
    #     st.session_state.df_filtered = st.session_state.dfData

    # # define column of interest to group and graph the dataframe
    # column_names_all = ["fuel_origin", "fuel_type", "fuel_type_name", "generator_type"]

    # # initialize selected columns and last valid selection for multiselect for function ensure_valid_selection
    # if "column_names_selec" not in st.session_state:
    #     st.session_state.column_names_selec = column_names_all
    # if "column_names_last_select" not in st.session_state:
    #     st.session_state.column_names_last_selec = column_names_all

    # # configure the sidebar
    # with st.sidebar:
    #     st.write("Navigation pages:")
    #     # pages
    #     st.page_link("main_page.py", label="Home")
    #     st.page_link("pages/1_electric_matrix.py", label="Electric Matrix")
    #     st.page_link("pages/2_hist_evol.py", label="Historical Evolution")
    #     st.page_link("pages/3_geo_distr.py", label="Geographic Distribution")

    # st.sidebar.divider()

    # with st.sidebar:
    #     # display filters to select
    #     st.write("Select the filters:")
    #     for filter_name in st.session_state.filters.keys():
    #         options = aux.get_filtered_options(
    #             st.session_state.dfData,
    #             filter_name,
    #             {k: v for k, v in st.session_state.filters.items() if k != filter_name},
    #         )
    #         st.session_state.filters[filter_name] = st.multiselect(
    #             f"Select {filter_name}",
    #             options=options,
    #             default=st.session_state.filters[filter_name],
    #         )

    #     # button to click to apply selected filters
    #     if st.button("Apply Filters"):
    #         st.session_state.df_filtered = aux.apply_filters_to_df(
    #             st.session_state.dfData,
    #             status=st.session_state.filters["status"],
    #             states=st.session_state.filters["states"],
    #             fuel_type=st.session_state.filters["fuel_type"],
    #             fuel_origin=st.session_state.filters["fuel_origin"],
    #             generator_type=st.session_state.filters["generator_type"],
    #             fuel_type_name=st.session_state.filters["fuel_type_name"],
    #         )

    # # title of the page
    # st.header("Brazilian electric matrix - Electric Matrix")

    # # select filters to group and graph
    # par_multi_category = st.multiselect(
    #     "Select columns to display in table:",
    #     options=column_names_all,
    #     default=st.session_state.column_names_selec,
    #     key="column_selector",
    #     on_change=update_column,
    #     args=(st.session_state.column_selector,),
    # )

    # par_selec_category = st.selectbox(
    #     "Select table column to graph:",
    #     options=st.session_state.column_names_selec,
    #     index=0,
    # )
    # # graphs title
    # st.subheader(f"Electric Power by {par_selec_category}")

    # # group dataframe for table and graphs
    # df_grouped = aux.groupby_func_to_df(
    #     st.session_state.df_filtered, st.session_state.column_names_selec
    # )

    # # manage colors for graphs
    # color_dict = vz.generate_color_dict_plotly(
    #     categories=st.session_state.dfData[par_selec_category].unique(),
    #     colormap="Pastel",
    # )

    # # graphs
    # c1, c2 = st.columns(2)
    # with c1:
    #     fig = vz.bar_plot_status_category(
    #         df_grouped, category=par_selec_category, color_dict=color_dict
    #     )
    #     st.plotly_chart(fig, use_container_width=True)

    # with c2:
    #     fig = vz.pie_plot_status_category(
    #         df_grouped, category=par_selec_category, color_dict=color_dict
    #     )
    #     st.plotly_chart(fig, use_container_width=True)

    # # display table
    # st.subheader("Table for total Electric Power")
    # st.table(df_grouped)


if __name__ == "__main__":
    main()
