"""All population and IMD data into one file.

Data from 2004-2017 to remain consistent with IMD
"""

import os

import pandas as pd
import numpy as np

__author__ = "Theo Rashid"
__email__ = "tar15@ic.ac.uk"

# Population and IMD data for 2004-2017
populations = []
for i in range(len(range(2004, 2017+1))):
    df = pd.read_csv("../Data/Populations/cleaned populations/pop_lsoa2011_" + str(2004 + i) + ".csv", index_col=0)
    populations.append(df)

IMD_2004_df = pd.read_csv("../Data/IMD/reaggregated IMD/IMD_LSOA11_2004.csv", index_col=0)
IMD_2007_df = pd.read_csv("../Data/IMD/reaggregated IMD/IMD_LSOA11_2007.csv", index_col=0)
IMD_2010_df = pd.read_csv("../Data/IMD/reaggregated IMD/IMD_LSOA11_2010.csv", index_col=0)
IMD_2015_df = pd.read_csv("../Data/IMD/reaggregated IMD/IMD_LSOA11_2015.csv", index_col=0)

# Stack populations on top
# Column for male or female
# Column for which age group

male_cols = list(populations[0].columns[1:20])
male_cols.insert(0, "LSOA2011")

female_cols = list(populations[0].columns[20:39])
female_cols.insert(0, "LSOA2011")

age_groups = populations[0].columns[1:20].str.replace("m", "")

def melt_pops(df):
    """Reshape population dfs to be stacked with age group and female levels
    """
    # Separate male and female, melt by age group
    m_df = df[male_cols]
    m_df.columns = m_df.columns.str.replace("m", "")
    m_df = pd.melt(m_df, id_vars="LSOA2011", value_vars=age_groups, var_name="age_group", value_name="population")
    m_df["sex"] = 1

    f_df = df[female_cols]
    f_df.columns = f_df.columns.str.replace("f", "")
    f_df = pd.melt(f_df, id_vars="LSOA2011", value_vars=age_groups, var_name="age_group", value_name="population")
    f_df["sex"] = 2

    melted_df = pd.concat([m_df, f_df],ignore_index=True)
    return melted_df

melted_pops = []
for i, df in enumerate(populations):
    melt_df = melt_pops(df)
    melt_df["YEAR"] = 2004+i
    melted_pops.append(melt_df)

population = pd.concat(melted_pops, ignore_index=True)

# Take the most recent available IMD data
# split up by year and merge, then concat back together
pop1 = population[population["YEAR"] < 2007]
pop2 = population[(population["YEAR"] >= 2007) & (population["YEAR"] < 2010)]
pop3 = population[(population["YEAR"] >= 2010) & (population["YEAR"] < 2015)]
pop4 = population[population["YEAR"] >= 2015]
pop1 = pop1.merge(IMD_2004_df, on="LSOA2011")
pop2 = pop2.merge(IMD_2007_df, on="LSOA2011")
pop3 = pop3.merge(IMD_2010_df, on="LSOA2011")
pop4 = pop4.merge(IMD_2015_df, on="LSOA2011")

population_IMD = pd.concat([pop1, pop2, pop3, pop4], ignore_index=True)

# add MSOA and LAD
geog_2011 = pd.read_csv("../Data/Geography/OA2011_lookup.csv", engine = "python")
geog_2011 = geog_2011[geog_2011["LAD11CD"].astype(str).str.startswith("E09")] # London only
geog_2011 = geog_2011[["LSOA11CD", "MSOA11CD", "LAD11CD"]]
geog_2011 = geog_2011.rename(columns={"LSOA11CD": "LSOA2011", "MSOA11CD": "MSOA2011", "LAD11CD": "LAD2011"})
geog_2011 = geog_2011.groupby(["LSOA2011"]).agg(lambda x:x.value_counts().index[0]) # at LSOA level

population_IMD = population_IMD.merge(geog_2011, on="LSOA2011")

population_IMD = population_IMD[["LAD2011", "MSOA2011", "LSOA2011", "YEAR", "age_group", "sex", "population",
                                "IMD score", "income score", "employment score"]]

# add ID columns to LAD, MSOA, LSOA, YEAR, age_group (start at 1 for modelling in R)
population_IMD["LAD id"] = population_IMD.groupby("LAD2011").ngroup() + 1 
population_IMD["MSOA id"] = population_IMD.groupby("MSOA2011").ngroup() + 1 
population_IMD["LSOA id"] = population_IMD.groupby("LSOA2011").ngroup() + 1 
population_IMD["YEAR id"] = population_IMD.groupby("YEAR").ngroup() + 1

age_group_id_dict = dict(zip(list(age_groups), range(1, 19+1)))
population_IMD["age_group id"] = population_IMD["age_group"].map(age_group_id_dict)

# population_IMD.to_csv("pop_IMD_2004_17.csv")
# geog_2011.to_csv("ldn_geog_lookup.csv")