import numpy as np
import pandas as pd


# define a filtering function
def apply_filters_to_df(
    df,
    status=None,
    states=None,
    fuel_type=None,
    fuel_origin=None,
    generator_type=None,
    fuel_type_name=None,
):
    """
    Apply the users filters to the dataframe for later visualizations.

    df: dataframe to be filtered.
    status(str or list of str, optional): Operative status of the power plant (Operative, Projected or In construction).
    state(str or list of str, optional): state of Brazil where is located the power plant.
    fuel_type(str or list of str, optional): specific fuel used in the power plant.
    fuel_origin(str or list of str, optional): general origin of the fuel used in the power plant, a more general clasification.
    generator_type(str or list of str, optional): type of electric generator used to generate electricity based in the fuel.

    return a filtered df
    """

    # define the filtered df
    df_filtered = df.copy()

    # define the conditions to filter
    if status:
        df_filtered = df_filtered[df_filtered["status"].isin(status)]
    if states:
        df_filtered = df_filtered[df_filtered["states"].isin(states)]
    if fuel_origin:
        df_filtered = df_filtered[df_filtered["fuel_origin"].isin(fuel_origin)]
    if fuel_type:
        df_filtered = df_filtered[df_filtered["fuel_type"].isin(fuel_type)]
    if fuel_type_name:
        df_filtered = df_filtered[df_filtered["fuel_type_name"].isin(fuel_type_name)]
    if generator_type:
        df_filtered = df_filtered[df_filtered["generator_type"].isin(generator_type)]

    # return the filtered dataframe
    return df_filtered


# define groupby function for graphs
def groupby_func_to_df(df, category):
    """
    Function to groupby acording to a category incerted as input. The category will be graph vs the
     sum of electric power inst.

    df: dataframe to groupby
    category: header of the column or list of header of columns to be group by.

    return a gropued dataframe
    """

    # direct dataframe
    df_grouped = df.copy()

    # apply groupby function
    df_grouped = (
        df_grouped.groupby(category).agg({"electric_power_inst": "sum"}).reset_index()
    )

    # return the df
    return df_grouped


# function for dynamic cascading or dependant filters
def get_filtered_options(df, column, filters):
    """
    df: The original dataframe
    column: The name of the column for which we want to get filtered options
    filters: A dictionary of current filter selections for other columns

    1
    It iterates through each filter in the filters dictionary:
    col is the name of a filter (e.g., 'fuel_origin', 'states')
    values is the list of selected values for that filter
    2
    If values is not empty (meaning some filter options are selected):
    It filters the dataframe to only include rows where the value in col is in the list of selected values
    3
    After applying all the filters, it returns a sorted list of unique values from the specified column of
    the resulting filtered dataframe
    """
    for col, values in filters.items():
        if values:
            df = df[df[col].isin(values)]

    return sorted(df[column].unique())


# function for forcing at least 1 option in a filter
def ensure_last_selection(new_selection, last_valid_selection):
    """
    This function ensures that at least 1 selection is maintained. The result of the selection ends in
    a graph function that will crash if nothing is selected. This way the user can't deselect everything
    and make the app crash

    new_selection: list of columns names selected
    last_valid_selection: list stored in session state with the last valid selection

    """
    if new_selection:
        return new_selection, new_selection
    return last_valid_selection, last_valid_selection
