# import libraries
import numpy as np
import pandas as pd
import geopandas as gpd
import plotly.express as px
import plotly.colors as pc
import plotly.graph_objects as go


# define function for manage colors in graphs
def generate_color_dict_plotly(categories, colormap):
    """
    Create a color dictionary for given variables using a specified Plotly color palette.

    :param variables: List of variable names
    :param palette_name: Name of the Plotly qualitative color palette to use (default is 'Plotly')
    :return: Dictionary mapping variables to colors
    """
    try:
        colors = getattr(px.colors.qualitative, colormap)
    except AttributeError:
        print(f"Palette '{colormap}' not found. Using default 'Plotly' palette.")
        colors = px.colors.qualitative.Plotly

    # Create the dictionary
    color_dict = {}
    for i, variable in enumerate(categories):
        color_dict[variable] = colors[i % len(colors)]

    return color_dict


def get_color_plotly(color_dict, categories):
    """
    Get colors for specified categories from a color dictionary.

    :param color_dict: Dictionary mapping categories to colors
    :param categories: List of categories to get colors for
    :return: List of colors for the specified categories
    """
    return [
        color_dict.get(category, "#000000") for category in categories
    ]  # Default to black if category not found


# define function for display choropleth map
def choropleth_mapbox_ele_pow(df, geodf, status, colors_scale):

    # # read procesed data
    # csv_file_path = r"C:\Users\Mariano\Documents\aprendizaje-data-science\repositorio-brazilian-electric-matrix\Brazilian-electric-matrix\data\processed\transformed_data.pkl"
    # df_aux = pd.read_pickle(csv_file_path)

    # # read geojson data
    # geojson_file_path_state = r"C:\Users\Mariano\Documents\aprendizaje-data-science\repositorio-brazilian-electric-matrix\Brazilian-electric-matrix\data\processed\all_states.geojson"
    # geojson_data_state = gpd.read_file(geojson_file_path_state)
    df_aux = df
    geojson_data_state = geodf
    # make dataframe for map
    df_sorted = (
        df_aux[df_aux["status"] == status]
        .groupby("states")
        .agg({"electric_power_inst": "sum", "electric_power_decl": "sum"})
        .reset_index()
    )

    # get better color for limits of the range in the color map
    key_min = np.percentile(df_sorted.electric_power_inst, 5)
    key_max = np.percentile(df_sorted.electric_power_inst, 95)

    # get the center of brazil to display by default
    state_bounds = geojson_data_state.geometry.total_bounds
    south, west, north, east = state_bounds

    # Calculate the center coordinates
    # center = {"lat": (south + north) / 2, "lon": (west + east) / 2}
    center = {"lat": -11.61, "lon": -51.81}
    # Calculate the zoom level
    zoom = 2.3  # Start with a zoom level of 4 (can be adjusted as needed)

    # create choropleth map
    fig = px.choropleth_mapbox(
        df_sorted,
        geojson=geojson_data_state,
        locations="states",
        featureidkey="properties.abbrev_state",
        color="electric_power_inst",
        color_continuous_scale=colors_scale,
        mapbox_style="carto-darkmatter",
        range_color=[key_min, key_max],
        center=center,
        zoom=zoom,
        opacity=1,
        labels={"electric_power_inst": "Electric Power KW"},
        # title=f"Electric Power by State by {status}",
    )
    fig.update_geos(fitbounds="locations", visible=False, scope="south america")

    # update layout atributes
    fig.update_layout(
        mapbox=dict(style="carto-darkmatter"),
        # paper_bgcolor="#343a40",
        # plot_bgcolor="#343a40",
        # font_color="white",
        legend=dict(title=dict(text="Legend Title"), orientation="h", x=1, y=1.02),
    )

    return fig


# define bar plot by status and category
def bar_plot_status_category(df, category, color_dict):

    # # read data
    # csv_file_path = r"C:\Users\Mariano\Documents\aprendizaje-data-science\repositorio-brazilian-electric-matrix\Brazilian-electric-matrix\data\processed\transformed_data.pkl"
    # df_aux = pd.read_pickle(csv_file_path)
    df_aux = df
    # make sorted dataframe
    df_sorted = (
        df_aux.groupby(category).agg({"electric_power_inst": "sum"}).reset_index()
    )
    # define colors
    # get unique values of categories
    # categories = list(df_aux[category].unique())
    # # get a dictionary with fix colors for each category
    # color_dict = generate_color_dict_plotly(categories=categories, colormap=color_scale)
    # color = get_color_plotly(color_dict=color_dict, categories=categories)
    # make bar graph
    fig = px.bar(
        df_sorted,
        x=category,
        y=df_sorted["electric_power_inst"] / 1000,
        color=category,
        color_discrete_map=color_dict,
        # title=f"Electric power by {status} and by {category}",
        labels={category: category, "y": "Electric Power (MW)"},
    )
    fig.update_layout(
        legend_title=None,
        showlegend=False,
        xaxis_title=None,
        # paper_bgcolor="#343a40",
        # plot_bgcolor="#343a40",
        # font_color="white",
    )
    fig.update_xaxes(tickangle=45)

    return fig


# #define pie plot by status and category
def pie_plot_status_category(df, category, color_dict):

    # # read data
    # csv_file_path = r"C:\Users\Mariano\Documents\aprendizaje-data-science\repositorio-brazilian-electric-matrix\Brazilian-electric-matrix\data\processed\transformed_data.pkl"
    # df_aux = pd.read_pickle(csv_file_path)
    df_aux = df
    # # generate colors for graphs
    # categories = list(df_aux[category].unique())
    # color_dict = generate_color_dict_plotly(categories=categories, colormap=color_scale)

    # make sorted dataframe
    df_sorted = (
        df_aux.groupby(category).agg({"electric_power_inst": "sum"}).reset_index()
    )

    # plot the pie graph
    fig = px.pie(
        df_sorted,
        values="electric_power_inst",
        names=category,
        # title=f"Electric Power by {status} and by {category}",
        color=category,
        color_discrete_map=color_dict,
        labels={category: category, "electric_power_inst": "Electric Power (KW)"},
    )

    fig.update_layout(
        # paper_bgcolor="#343a40",
        # plot_bgcolor="#343a40",
        # font_color="white",
    )

    return fig


# #define historical line plot
def hist_line_plot(df, category, color_scale):

    # read data
    # csv_file_path = r"C:\Users\Mariano\Documents\aprendizaje-data-science\repositorio-brazilian-electric-matrix\Brazilian-electric-matrix\data\processed\transformed_data.pkl"
    # df_aux = pd.read_pickle(csv_file_path)
    df_aux = df
    # generate colors for graph
    categories = df_aux[category].unique()
    color_dict = generate_color_dict_plotly(categories=categories, colormap=color_scale)

    # for this graph, only take into consideration operative power plants
    df_sorted = df_aux[df_aux["status"] == "Operação"]
    # get the year of the datetime column to do a groupby

    df_sorted["Year"] = df_sorted["DatEntradaOperacao"].dt.year

    # group by year and category and summ the electric power
    df_sorted = (
        df_sorted.groupby(["Year", category])["electric_power_inst"].sum().reset_index()
    )
    df_sorted = df_sorted.sort_values("Year")
    # calculate cumulative sum of the power by category
    df_sorted["Cumulative_Power"] = df_sorted.groupby(category)[
        "electric_power_inst"
    ].cumsum()

    # create a dataframe with all the years from min to max date with every category combination
    year_range = range(df_sorted["Year"].min(), df_sorted["Year"].max() + 1)
    df_all_years = pd.DataFrame(
        [(year, cat) for year in year_range for cat in categories],
        columns=["Year", category],
    )

    # merge dataframe with cumulative electric power with dataframe with all years
    df_historic = pd.merge(
        df_all_years,
        df_sorted[["Year", category, "Cumulative_Power"]],
        on=["Year", category],
        how="left",
    )

    # fill forward cumulative values to fill NaN or 0 gaps
    df_historic["Cumulative_Power"] = df_historic.groupby(category)[
        "Cumulative_Power"
    ].ffill()

    # fill any remaining NaN value with 0, specially the first values not filled before
    df_historic["Cumulative_Power"] = df_historic["Cumulative_Power"].fillna(0)

    # Create the stacked area chart
    fig = px.area(
        df_historic,
        x="Year",
        y="Cumulative_Power",
        color=category,
        color_discrete_map=color_dict,
        labels={
            "Cumulative_Power": "Installed Power (kW)",
            category: category,
        },
        # title=f"Historical Evolution of Installed Electric Power by {category}",
    )

    # Customize the layout
    fig.update_layout(
        # xaxis_title="Year",
        yaxis_title="Total Installed Power (kW)",
        legend_title=category,
        hovermode="x unified",
        # paper_bgcolor="#343a40",
        # plot_bgcolor="#343a40",
        # font_color="white",
    )

    return fig


# define location map for every generator
def loc_map_plot(df, geodf, status, category, color_scale):

    # # read data
    # csv_file_path = r"C:\Users\Mariano\Documents\aprendizaje-data-science\repositorio-brazilian-electric-matrix\Brazilian-electric-matrix\data\processed\transformed_data.pkl"
    # df_aux = pd.read_pickle(csv_file_path)

    # # read geojson data
    # geojson_file_path_state = r"C:\Users\Mariano\Documents\aprendizaje-data-science\repositorio-brazilian-electric-matrix\Brazilian-electric-matrix\data\processed\all_states.geojson"
    # geojson_data_state = gpd.read_file(geojson_file_path_state)
    df_aux = df
    geojson_data_state = geodf

    # define colors for graph
    categories = df_aux[category].unique()
    color_dict = generate_color_dict_plotly(categories=categories, colormap=color_scale)

    # filter dataframe
    df_filtered = df_aux[df_aux["status"] == status]

    # create colormap for points of location by category
    color_discrete_map = {
        cat: color
        for cat, color in color_dict.items()
        if cat in df_filtered[category].unique()
    }

    # Calculate the center coordinates
    center = {"lat": -11.61, "lon": -51.81}

    # Calculate the zoom level
    zoom = 2.5  # Start with a zoom level of 4 (can be adjusted as needed)

    # Create the base map
    fig = px.choropleth_mapbox(
        geojson_data_state,
        geojson=geojson_data_state.geometry,
        locations=geojson_data_state.index,
        mapbox_style="carto-darkmatter",
        zoom=zoom,
        center=center,
        opacity=0.2,
    )
    # delete the legend of the choropleth
    fig.data[0].showlegend = False

    # Add scatter plot for location points of power plants
    for cat in categories:
        category_data = df_filtered[df_filtered[category] == cat]
        fig.add_trace(
            go.Scattermapbox(
                lat=category_data["latitude"],
                lon=category_data["longitude"],
                mode="markers",
                marker=dict(size=5, color=color_dict[cat]),
                text=category_data.apply(
                    lambda row: f"Name: {row['NomEmpreendimento']}<br>"
                    f"Elec. Power: {row['electric_power_inst']:.2f} kW<br>"
                    f"Lat: {row['latitude']:.4f}<br>"
                    f"Lon: {row['longitude']:.4f}",
                    axis=1,
                ),
                name=cat,  # This will appear in the legend
                hoverinfo="text",
            )
        )

    # Update layout
    # fig.update_layout(
    #     title="Power Plants in Brazil",
    #     legend_title="Power Plants",
    #     # paper_bgcolor="#343a40",
    #     # plot_bgcolor="#343a40",
    #     # font_color="white",
    # )

    return fig
