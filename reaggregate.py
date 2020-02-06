"""Function to reaggreate from source to target geographies."""

import pandas as pd

__author__ = "Theo Rashid"
__email__ = "tar15@ic.ac.uk"

def reaggregator(source_geog, target_geog, value_col, geog_df, value_df):
    """Function to reaggregate from source (old) to target (new) geographies
    using a common unit between them (in the geog_df).
    The function works by assigning the value from the source to each common unit (smaller)
    between the source and the target geographies. We then group the common unit values by
    target geograpghy, taking the mean value (sum across all common units in the target
    geography divided by the number of common units in the target geography).

    Keyword arguments:
    source_geog -- column name of the source geography
    target_geog -- column name of the target geography
    ####################################
    """

    # MERGE geog_df and value_df (only with value_col) on source_geog
    # This will assign each common unit with the value

    # GROUP (common units) BY target_geog
    # Sum the values
    # Count the number of postcodes
    # new value = sum/num_postcodes

