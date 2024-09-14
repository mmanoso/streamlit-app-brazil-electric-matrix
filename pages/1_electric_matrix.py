import pandas as pd
import numpy as np

# import plotly.express as px
import streamlit as st
import streamlit_dynamic_filters as stdf
from typing import List, Dict, Any
import visualization_func as vz  # visualization functions for graphs
import aux_func as aux  # auxiliary functions for manage data
import config  # import file paths and constants


# # callbackfunction for sidebar filters
# def update_filters_sidebar(filter_name, selected_options):
#     """Ensures the inmediate writing of the filter to avoid having to click 2 times"""
#     st.session_state.filters[filter_name] = selected_options
# callback to reset filters and apply changes to dataframe
def reset_filters():
    if "filters" in st.session_state:
        st.session_state.filters = {
            "status": [],
            "fuel_origin": [],
            "fuel_type": [],
            "fuel_type_name": [],
            "generator_type": [],
            "states": [],
        }


# initialize session state variables
@st.cache_data
def initialize_session_state_data() -> None:
    """Initialize session state variables"""
    # data
    if "dfData" not in st.session_state:
        try:
            st.session_state.dfData = pd.read_pickle(config.csv_file_path)
        except Exception as e:
            st.error(f"Error loading data: {str(e)}")
            st.stop()


def reinitialize_session_state_filters() -> None:
    # filters
    if "filters" in st.session_state:
        st.session_state.filters = {
            "status": [],
            "fuel_origin": [],
            "fuel_type": [],
            "fuel_type_name": [],
            "generator_type": [],
            "states": [],
        }


def initialize_session_state_variables() -> None:
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
    if "groupby_columns" not in st.session_state:
        st.session_state.groupby_columns = config.groupby_column_names

    # selection of column for graph
    if "graph_column" not in st.session_state:
        st.session_state.graph_column = config.groupby_column_names[0]


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
    #             key=filter_name,
    #             on_change=update_filters_sidebar,
    #             args=(filter_name, st.session_state.filters[filter_name]),
    #         )
    #         st.write(f"Selected {filter_name}: {st.session_state.filters[filter_name]}")
    #         st.write(f"Selected {filter_name}: {options}")
    #     # button to click to apply selected filters
    #     c1, c2 = st.columns(2)
    #     with c1:
    #         # button to click to apply selected filters
    #         if st.button("Apply Filters"):
    #             apply_filters()
    #     with c2:
    #         # button to click to reset all filters at once
    #         if st.button("Reset Filters"):
    #             reset_filters()


# def apply_filters() -> None:
#     """Apply selected filters to the dataframe"""
#     try:
#         st.session_state.df_filtered = aux.apply_filters_to_df(
#             st.session_state.dfData, **st.session_state.filters
#         )
#     except Exception as e:
#         st.error(f"Error applying filters: {str(e)}")


# # define function for button of reset filter in sidebar
# def reset_filters() -> None:
#     """Reset all selected filters for the dataframe"""
#     try:
#         st.session_state.filters = {
#             "status": [],
#             "fuel_origin": [],
#             "fuel_type": [],
#             "fuel_type_name": [],
#             "generator_type": [],
#             "states": [],
#         }
#         apply_filters()
#     except Exception as e:
#         st.error(f"Error reseting filters: {str(e)}")


# function for render the main content of the page
def render_main_content() -> None:
    """Render the main content of the page"""
    # title of the page
    st.header("Brazilian electric matrix - Electric Matrix")
    # select filters to group and graph
    groupby_columns = st.multiselect(
        "Select columns to display in table:",
        options=config.groupby_column_names,
        default=st.session_state.groupby_columns,
        key="groupby_columns",
    )

    if st.session_state.groupby_columns:
        st.session_state.graph_column = st.selectbox(
            "Select table column to graph:",
            options=st.session_state.groupby_columns,
            index=0,
        )

        df_grouped = aux.groupby_func_to_df(
            st.session_state.df_filtered, st.session_state.groupby_columns
        )

        render_visualization(df_grouped, st.session_state.graph_column)
        render_table(df_grouped)
    else:
        st.warning("Please select at least one column to group by.")


def render_visualization(df_grouped: pd.DataFrame, category: str) -> None:
    """Render the graphs based on the grouped data"""
    if not df_grouped.empty and category in df_grouped.columns:

        # manage the color dictionary for the data
        color_dict = vz.generate_color_dict_plotly(
            categories=st.session_state.dfData[category].unique(),
            colormap="Safe",
        )

        c1, c2 = st.columns([0.4, 0.6])
        with c1:
            fig = vz.pie_plot_status_category(df_grouped, category, color_dict)
            st.plotly_chart(fig, use_container_width=True)
        with c2:
            fig = vz.bar_plot_status_category(df_grouped, category, color_dict)
            st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("No data available for visualization.")


def render_table(df_grouped: pd.DataFrame) -> None:
    """Render the table (dataframe) based on the grouped data"""
    if not df_grouped.empty:

        st.subheader("Table for total Electric Power")
        st.table(df_grouped)
    else:
        st.warning("No data available for the table")


def main() -> None:
    """Main function to run the streamlit app in Page 1 Electric Matrix"""
    # initial config parameters of the web page
    st.set_page_config(
        page_title="Brazilian electric matrix analysis",
        page_icon=":bar_chart:",
        layout="wide",
        initial_sidebar_state="expanded",
    )

    initialize_session_state_data()

    initialize_session_state_variables()
    dynamic_filters = stdf.DynamicFilters(
        st.session_state.dfData,
        filters=config.dynamic_filter_column_names,
        filters_name="filters",
    )
    dynamic_filters.check_state()

    with st.sidebar:
        st.write("Navigation pages:")
        # pages
        st.page_link("main_page.py", label="Home")
        st.page_link("pages/1_electric_matrix.py", label="Electric Matrix")
        st.page_link("pages/2_hist_evol.py", label="Historical Evolution")
        st.page_link("pages/3_geo_distr.py", label="Geographic Distribution")

    st.sidebar.divider()

    dynamic_filters.display_filters("sidebar")
    with st.sidebar:
        if st.button("Reset Filters"):
            reinitialize_session_state_filters()
            st.rerun()
    # dynamic_filters.display_df()
    # st.dataframe(dynamic_filters.display_df())
    st.session_state.df_filtered = dynamic_filters.filter_df()
    render_main_content()


if __name__ == "__main__":
    main()
