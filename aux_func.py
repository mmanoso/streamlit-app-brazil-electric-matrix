import numpy as np
import pandas as pd
from typing import Dict, List, Any, Optional, Tuple, Union


# define a filtering function
def apply_filters_to_df(
    df: pd.DataFrame,
    status: Optional[List[str]] = None,
    states: Optional[List[str]] = None,
    fuel_type: Optional[List[str]] = None,
    fuel_origin: Optional[List[str]] = None,
    generator_type: Optional[List[str]] = None,
    fuel_type_name: Optional[List[str]] = None,
) -> pd.DataFrame:
    """
    Apply the users filters to the dataframe for later visualizations.

    Args:
        df (pd.DataFrame): DataFrame to be filtered.
        status (Optional[List[str]]): Operative status of the power plant.
        states (Optional[List[str]]): States of Brazil where the power plants are located.
        fuel_type (Optional[List[str]]): Specific fuel used in the power plant.
        fuel_origin (Optional[List[str]]): General origin of the fuel used in the power plant.
        generator_type (Optional[List[str]]): Type of electric generator used.
        fuel_type_name (Optional[List[str]]): Name of the fuel type.

    Returns:
        pd.DataFrame: Filtered DataFrame

    """

    # define the filtered df
    df_filtered = df.copy()

    # create dictionary of filters
    filter_conditions = {
        "status": status,
        "states": states,
        "fuel_origin": fuel_origin,
        "fuel_type": fuel_type,
        "fuel_type_name": fuel_type_name,
        "generator_type": generator_type,
    }

    for column, values in filter_conditions.items():
        if values:
            df_filtered = df_filtered[df_filtered[column].isin(values)]

    return df_filtered


# define groupby function for graphs
def groupby_func_to_df(
    df: pd.DataFrame, category: Union[str, List[str]]
) -> pd.DataFrame:
    """
    Group the DataFrame by a category and sum the electric power.

    Args:
        df (pd.DataFrame): DataFrame to group
        category (Union[str, List[str]]): Column(s) to group by

    Returns:
        pd.DataFrame: Grouped DataFrame
    """
    return df.groupby(category).agg({"electric_power_inst": "sum"}).reset_index()


# function for dynamic cascading or dependant filters
def get_filtered_options(
    df: pd.DataFrame, column: str, filters: Dict[str, List[str]]
) -> List[str]:
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

    Args:
        df (pd.DataFrame): The original DataFrame
        column (str): The name of the column for which we want to get filtered options
        filters (Dict[str, List[str]]): A dictionary of current filter selections for other columns

    Returns:
        List[str]: Sorted list of unique values from the specified column
    """
    for col, values in filters.items():
        if values:
            df = df[df[col].isin(values)]

    return sorted(df[column].unique())


# function for forcing at least 1 option in a filter
def ensure_last_selection(
    new_selection: List[str], last_valid_selection: List[str]
) -> Tuple[List[str], List[str]]:
    """
    Ensure that at least 1 selection is maintained.

    Args:
        new_selection (List[str]): List of columns names selected
        last_valid_selection (List[str]): List stored in session state with the last valid selection

    Returns:
        Tuple[List[str], List[str]]: Tuple containing the current selection and the last valid selection
    """
    if new_selection:
        return new_selection, new_selection
    return last_valid_selection, last_valid_selection
