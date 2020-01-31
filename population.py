import os
import pandas as pd
import numpy as np

# Files between 2012-2017 are of the same file type with a different sheet for males and females and a population estimate for each age until 90+
males_dfs = []
females_dfs = []
for year in range(2012, 2017+1):
    males_df = pd.read_excel("../Data/Populations/pop{0!s}_lsoa2011.xls".format(year), sheet_name = "Mid-{0!s} Males".format(year),  engine = 'xlrd', skiprows = 4)
    males_df = males_df.dropna(subset=["Unnamed: 2"])
    females_df = pd.read_excel("../Data/Populations/pop{0!s}_lsoa2011.xls".format(year), sheet_name = "Mid-{0!s} Females".format(year),  engine = 'xlrd', skiprows = 4)
    females_df = females_df.dropna(subset=["Unnamed: 2"])

    # Sum into five year age groups (and 85+)
    age_groups_list = np.array_split(range(85), 17) # splits into groups of 5 years

    for group in age_groups_list:
        males_df["m" + str(min(group)) + "_" + str(max(group))] = males_df.loc[:, group].sum(axis=1)
    males_df["m85+"] = males_df.loc[:, [85, 86, 87, 88, 89, "90+"]].sum(axis=1) # separate for 85+ column

    males_df.drop(males_df.columns[1:95], axis=1, inplace=True) # Keep only the LSOA code and summed columns
    males_dfs.append(males_df)

    for group in age_groups_list:
        females_df["f" + str(min(group)) + "_" + str(max(group))] = females_df.loc[:, group].sum(axis=1)
    females_df["f85+"] = females_df.loc[:, [85, 86, 87, 88, 89, "90+"]].sum(axis=1) # separate for 85+ column

    females_df.drop(females_df.columns[1:95], axis=1, inplace=True) # Keep only the LSOA code and summed columns
    females_dfs.append(females_df)