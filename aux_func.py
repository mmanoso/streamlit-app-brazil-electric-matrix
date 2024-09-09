import numpy as np
import pandas as pd


# define a filtering function
def apply_filters_to_df(
    df, status=None, state=None, fuel_type=None, fuel_origin=None, generator_type=None
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
        df_filtered = df_filtered[df_filtered["Status"].isin(status)]
    if state:
        df_filtered = df_filtered[df_filtered["State"].isin(state)]
    if fuel_origin:
        df_filtered = df_filtered[df_filtered["fuel_origin"].isin(fuel_origin)]
    if fuel_type:
        df_filtered = df_filtered[df_filtered["fuel_type"].isin(fuel_type)]
    if generator_type:
        df_filtered = df_filtered[df_filtered["generator_type"].isin(generator_type)]

    # return the filtered dataframe
    return df_filtered
