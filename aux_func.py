import numpy as np
import pandas as pd
from typing import Dict, List, Any, Optional, Tuple, Union
import streamlit as st


# class DynamicFilters:
#     """
#     A class to create dynamic multi-select filters in Streamlit.

#     ...

#     Attributes
#     ----------
#     df : DataFrame
#         The dataframe on which filters are applied.
#     filters : dict
#         Dictionary with filter names as keys and their selected values as values.

#     Methods
#     -------
#     check_state():
#         Initializes the session state with filters if not already set.
#     filter_df(except_filter=None):
#         Returns the dataframe filtered based on session state excluding the specified filter.
#     display():
#         Renders the dynamic filters and the filtered dataframe in Streamlit.
#     """

#     def __init__(self, df, filters, filters_name="filters"):
#         """
#         Constructs all the necessary attributes for the DynamicFilters object.

#         Parameters
#         ----------
#             df : DataFrame
#                 The dataframe on which filters are applied.
#             filters : list of filters
#                 List of columns names in df for which filters are to be created.
#             filters_name: str, optional
#                 Name of the filters object in session state.
#         """
#         self.df = df
#         self.filters_name = filters_name
#         self.filters = {filter_name: [] for filter_name in filters}
#         self.check_state()

#     def check_state(self):
#         """Initializes the session state with filters if not already set."""
#         # if 'filters' not in st.session_state:
#         #     st.session_state.filters = self.filters
#         if self.filters_name not in st.session_state:
#             st.session_state[self.filters_name] = self.filters

#     def reset_filters(self):
#         """
#         Resets the current filter.

#         Can be called using a button:

#             st.button("Reset Filters", on_click=dynamic_filters.reset_filters)

#         """
#         if self.filters_name in st.session_state:
#             del st.session_state[self.filters_name]

#     def filter_df(self, except_filter=None):
#         """
#         Filters the dataframe based on session state values except for the specified filter.

#         Parameters
#         ----------
#             except_filter : str, optional
#                 The filter name that should be excluded from the current filtering operation.

#         Returns
#         -------
#             DataFrame
#                 Filtered dataframe.
#         """
#         filtered_df = self.df.copy()
#         for key, values in st.session_state[self.filters_name].items():
#             if key != except_filter and values:
#                 filtered_df = filtered_df[filtered_df[key].isin(values)]
#         return filtered_df

#     def display_filters(self, location=None, num_columns=0, gap="small"):
#         """
#         Renders dynamic multiselect filters for user selection.

#         Parameters:
#         -----------
#         location : str, optional
#             The location where the filters are to be displayed. Accepted values are:
#             - 'sidebar': Displays filters in the side panel of the application.
#             - 'columns': Displays filters in columns format in the main application area.
#             - None: Defaults to main application area without columns.
#             Default is None.

#         num_columns : int, optional
#             The number of columns in which filters are to be displayed when location is set to 'columns'.
#             Constraints:
#             - Must be an integer.
#             - Must be less than or equal to 8.
#             - Must be less than or equal to the number of filters + 1.
#             If location is 'columns', this value must be greater than 0.
#             Default is 0.

#         gap : str, optional
#             Specifies the gap between columns when location is set to 'columns'. Accepted values are:
#             - 'small': Minimal gap between columns.
#             - 'medium': Moderate gap between columns.
#             - 'large': Maximum gap between columns.
#             Default is 'small'.

#         Behavior:
#         ---------
#         - The function iterates through session-state filters.
#         - For each filter, the function:
#             1. Generates available filter options based on the current dataset.
#             2. Displays a multiselect box for the user to make selections.
#             3. Updates the session state with the user's selection.
#         - If any filter value changes, the application triggers an update to adjust other filter options based on the current selection.
#         - If a user's previous selection is no longer valid based on the dataset, it's removed.
#         - If any filters are updated, the application will rerun for the changes to take effect.

#         Exceptions:
#         -----------
#         Raises StreamlitAPIException if the provided arguments don't meet the required constraints.

#         Notes:
#         ------
#         The function uses Streamlit's session state to maintain user's selections across reruns.
#         """
#         # # error handling
#         # if location not in ["sidebar", "columns", None]:
#         #     raise st.error.StreamlitAPIException(
#         #         "location must be either 'sidebar' or 'columns'"
#         #     )
#         # # if num_columns is not integer
#         # if not isinstance(num_columns, int):
#         #     raise st.error.StreamlitAPIException("num_columns must be an integer")
#         # # if num_columns is greater than 8
#         # if num_columns > 8:
#         #     raise st.error.StreamlitAPIException(
#         #         "num_columns must be less than or equal to 8"
#         #     )
#         # # if num_columns is greater than the number of filters
#         # if num_columns > len(st.session_state[self.filters_name]) + 1:
#         #     raise st.error.StreamlitAPIException(
#         #         "num_columns must be less than or equal to the number of filters"
#         #     )
#         # # if location is column and num_columns is 0
#         # if location == "columns" and num_columns == 0:
#         #     raise st.error.StreamlitAPIException(
#         #         "num_columns must be greater than 0 when location is 'columns'"
#         #     )
#         # if gap not in ["small", "medium", "large"]:
#         #     raise st.error.StreamlitAPIException(
#         #         "gap must be either 'small', 'medium' or 'large'"
#         #     )

#         filters_changed = False

#         # initiate counter and max_value for columns
#         if location == "columns" and num_columns > 0:
#             counter = 1
#             max_value = num_columns
#             col_list = st.columns(num_columns, gap=gap)

#         for filter_name in st.session_state[self.filters_name].keys():
#             filtered_df = self.filter_df(filter_name)
#             options = filtered_df[filter_name].unique().tolist()

#             # Remove selected values that are not in options anymore
#             valid_selections = [
#                 v
#                 for v in st.session_state[self.filters_name][filter_name]
#                 if v in options
#             ]
#             if valid_selections != st.session_state[self.filters_name][filter_name]:
#                 st.session_state[self.filters_name][filter_name] = valid_selections
#                 filters_changed = True

#             if location == "sidebar":
#                 with st.sidebar:
#                     selected = st.multiselect(
#                         f"Select {filter_name}",
#                         sorted(options),
#                         default=st.session_state[self.filters_name][filter_name],
#                         key=self.filters_name + filter_name,
#                     )
#             elif location == "columns" and num_columns > 0:
#                 with col_list[counter - 1]:
#                     selected = st.multiselect(
#                         f"Select {filter_name}",
#                         sorted(options),
#                         default=st.session_state[self.filters_name][filter_name],
#                         key=self.filters_name + filter_name,
#                     )

#                 # increase counter and reset to 1 if max_value is reached
#                 counter += 1
#                 counter = counter % (max_value + 1)
#                 if counter == 0:
#                     counter = 1
#             else:
#                 selected = st.multiselect(
#                     f"Select {filter_name}",
#                     sorted(options),
#                     default=st.session_state[self.filters_name][filter_name],
#                     key=self.filters_name + filter_name,
#                 )

#             if selected != st.session_state[self.filters_name][filter_name]:
#                 st.session_state[self.filters_name][filter_name] = selected
#                 filters_changed = True

#         if filters_changed:
#             st.rerun()

#     def display_df(self, **kwargs):
#         """Renders the filtered dataframe in the main area."""
#         # Display filtered DataFrame
#         st.dataframe(self.filter_df(), **kwargs)


# class DynamicFiltersHierarchical(DynamicFilters):
#     """
#     A class that extends DynamicFilters to create dynamic multi-select filters in Streamlit with hierarchical dependencies.

#     This class allows for the creation of filters where the selection in one filter impacts the options available in subsequent filters, forming a hierarchical structure of dependency.

#     Inherits from:
#     DynamicFilters - The base class for creating dynamic filters.

#     Attributes:
#     Inherits all attributes from DynamicFilters.

#     Methods:
#     Extends or overrides the following methods from DynamicFilters.
#     """

#     def filter_df(self, except_filter=None, except_filter_tab: list = None):
#         """
#         Filters the dataframe based on session state values except for specified filters.

#         This method extends the filter_df method from DynamicFilters by adding an additional parameter to handle hierarchical dependencies among filters.

#         Parameters
#         ----------
#         except_filter : str, optional
#             The filter name that should be excluded from the current filtering operation. This is useful when updating filter options dynamically.

#         except_filter_tab : list, optional
#             A list of filter names that should be excluded from the current filtering operation. This is crucial for maintaining hierarchical dependencies.

#         Returns
#         -------
#         DataFrame
#             The filtered dataframe based on current selections in session state, excluding specified filters.
#         """

#         if except_filter_tab is None:
#             except_filter_tab = []
#         filtered_df = self.df.copy()
#         for key, values in st.session_state[self.filters_name].items():
#             if key != except_filter and key not in except_filter_tab and values:
#                 filtered_df = filtered_df[filtered_df[key].isin(values)]
#         return filtered_df

#     def display_filters(self, location=None, num_columns=0, gap="small"):
#         """
#         Renders dynamic multiselect filters for user selection.

#         Parameters:
#         -----------
#         location : str, optional
#             The location where the filters are to be displayed. Accepted values are:
#             - 'sidebar': Displays filters in the side panel of the application.
#             - 'columns': Displays filters in columns format in the main application area.
#             - None: Defaults to main application area without columns.
#             Default is None.

#         num_columns : int, optional
#             The number of columns in which filters are to be displayed when location is set to 'columns'.
#             Constraints:
#             - Must be an integer.
#             - Must be less than or equal to 8.
#             - Must be less than or equal to the number of filters + 1.
#             If location is 'columns', this value must be greater than 0.
#             Default is 0.

#         gap : str, optional
#             Specifies the gap between columns when location is set to 'columns'. Accepted values are:
#             - 'small': Minimal gap between columns.
#             - 'medium': Moderate gap between columns.
#             - 'large': Maximum gap between columns.
#             Default is 'small'.

#         Behavior:
#         ---------
#         - The function iterates through session-state filters.
#         - For each filter, the function:
#             1. Generates available filter options based on the current dataset.
#             2. Displays a multiselect box for the user to make selections.
#             3. Updates the session state with the user's selection.
#         - If any filter value changes, the application triggers an update to adjust other filter options based on the current selection.
#         - If a user's previous selection is no longer valid based on the dataset, it's removed.
#         - If any filters are updated, the application will rerun for the changes to take effect.

#         Exceptions:
#         -----------
#         Raises StreamlitAPIException if the provided arguments don't meet the required constraints.

#         Notes:
#         ------
#         The function uses Streamlit's session state to maintain user's selections across reruns.
#         """
#         # error handling
#         if location not in ["sidebar", "columns", None]:
#             raise st.error.StreamlitAPIException(
#                 "location must be either 'sidebar' or 'columns'"
#             )
#         # if num_columns is not integer
#         if not isinstance(num_columns, int):
#             raise st.error.StreamlitAPIException("num_columns must be an integer")
#         # if num_columns is greater than 8
#         if num_columns > 8:
#             raise st.error.StreamlitAPIException(
#                 "num_columns must be less than or equal to 8"
#             )
#         # if num_columns is greater than the number of filters
#         if num_columns > len(st.session_state[self.filters_name]) + 1:
#             raise st.error.StreamlitAPIException(
#                 "num_columns must be less than or equal to the number of filters"
#             )
#         # if location is column and num_columns is 0
#         if location == "columns" and num_columns == 0:
#             raise st.error.StreamlitAPIException(
#                 "num_columns must be greater than 0 when location is 'columns'"
#             )
#         if gap not in ["small", "medium", "large"]:
#             raise st.error.StreamlitAPIException(
#                 "gap must be either 'small', 'medium' or 'large'"
#             )

#         filters_changed = False

#         # initiate counter and max_value for columns
#         if location == "columns" and num_columns > 0:
#             counter = 1
#             max_value = num_columns
#             col_list = st.columns(num_columns, gap=gap)

#         hierarchical_filter_name = list(st.session_state[self.filters_name].keys())
#         for filter_name in st.session_state[self.filters_name].keys():
#             filtered_df = self.filter_df(except_filter_tab=hierarchical_filter_name)
#             hierarchical_filter_name.remove(filter_name)
#             options = filtered_df[filter_name].unique().tolist()

#             # Remove selected values that are not in options anymore
#             valid_selections = [
#                 v
#                 for v in st.session_state[self.filters_name][filter_name]
#                 if v in options
#             ]
#             if valid_selections != st.session_state[self.filters_name][filter_name]:
#                 st.session_state[self.filters_name][filter_name] = valid_selections
#                 filters_changed = True

#             if location == "sidebar":
#                 with st.sidebar:
#                     selected = st.multiselect(
#                         f"Select {filter_name}",
#                         sorted(options),
#                         default=st.session_state[self.filters_name][filter_name],
#                         key=self.filters_name + filter_name,
#                     )
#             elif location == "columns" and num_columns > 0:
#                 with col_list[counter - 1]:
#                     selected = st.multiselect(
#                         f"Select {filter_name}",
#                         sorted(options),
#                         default=st.session_state[self.filters_name][filter_name],
#                         key=self.filters_name + filter_name,
#                     )

#                 # increase counter and reset to 1 if max_value is reached
#                 counter += 1
#                 counter = counter % (max_value + 1)
#                 if counter == 0:
#                     counter = 1
#             else:
#                 selected = st.multiselect(
#                     f"Select {filter_name}",
#                     sorted(options),
#                     default=st.session_state[self.filters_name][filter_name],
#                     key=self.filters_name + filter_name,
#                 )

#             if selected != st.session_state[self.filters_name][filter_name]:
#                 st.session_state[self.filters_name][filter_name] = selected
#                 filters_changed = True

#         if filters_changed:
#             st.rerun()

#     def display_df(self, **kwargs):
#         """Renders the filtered dataframe in the main area."""
#         # Display filtered DataFrame
#         st.dataframe(self.filter_df(), **kwargs)


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
