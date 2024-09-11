import pandas as pd
import numpy as np
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

# initialize filters in session state for dynamic filters
if "filters" not in st.session_state:
    st.session_state.filters = {
        "status": [],
        "fuel_origin": [],
        "fuel_type": [],
        "fuel_type_name": [],
        "generator_type": [],
        "states": [],
    }
# initialize dataframe in session state for dynamic filtering
if "df_filtered" not in st.session_state:
    st.session_state.df_filtered = dfData

# define column of interest to group and graph the dataframe
column_names = ["fuel_origin", "fuel_type", "fuel_type_name", "generator_type"]

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
            dfData,
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
            dfData,
            status=st.session_state.filters["status"],
            states=st.session_state.filters["states"],
            fuel_type=st.session_state.filters["fuel_type"],
            fuel_origin=st.session_state.filters["fuel_origin"],
            generator_type=st.session_state.filters["generator_type"],
            fuel_type_name=st.session_state.filters["fuel_type_name"],
        )

# title of the page
st.header("Brazilian electric matrix - Electric Matrix")

# select filters to group and graph
par_multi_category = st.multiselect(
    "Select columns to display in table:", options=column_names, default=column_names
)
par_selec_category = st.selectbox(
    "Select table column to graph:", options=par_multi_category, index=0
)
# graphs title
st.subheader(f"Electric Power by {par_selec_category}")

# group dataframe for table and graphs
df_grouped = aux.groupby_func_to_df(st.session_state.df_filtered, par_multi_category)

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
