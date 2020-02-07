"""Function to reaggreate from source to target geographies."""

import pandas as pd

__author__ = "Theo Rashid"
__email__ = "tar15@ic.ac.uk"

def reaggregator(source_geog, target_geog, geog_df, value_df):
    """Function to reaggregate from source (old) to target (new) geographies
    using a common unit between them (in the geog_df).
    The function works by assigning the value from the source to each common unit (smaller)
    between the source and the target geographies. We then group the common unit values by
    target geograpghy, taking the mean value (sum across all common units in the target
    geography divided by the number of common units in the target geography).


    Keyword arguments:
    source_geog -- column name of the source geography
    target_geog -- column name of the target geography
    geog_df -- dataframe containing the source and target geographies
    values_df -- dataframe containing the scores to be reaggregated

    THIS METHOD CURRENTLY ONLY WORKS WITH THE DATA REQUIRED
    IT WILL ONLY SUM OVER IMD, INCOME AND UNEMPLOYMENT FOR THE COMMON POSTCODE/GID UNIT
    IT WILL HAVE TO BE ADAPTED TO PERFORM SUMMATION OVER OTHER INDICATORS OR USING OTHER
    COMMON UNITS
    """

    # MERGE geog_df and value_df on source_geog
    # This will assign each common unit (postcode) with the value
    df = geog_df.merge(value_df, on = source_geog)

    # GROUP (postcodes) BY target_geog, sum the scores and 
    # Count the number of postcodes (or equivalently gid)
    agg_df = df.groupby([target_geog]).agg({"IMD score":"sum",
                                            "income score":"sum",
                                            "employment score":"sum",
                                            "gid":"count"}).reset_index()

    # new score = sum of scores in target_geog/number of postcodes in target_geog
    agg_df["IMD score"]        = agg_df["IMD score"]/agg_df["gid"]
    agg_df["income score"]     = agg_df["income score"]/agg_df["gid"]
    agg_df["employment score"] = agg_df["employment score"]/agg_df["gid"]

    return agg_df
    
