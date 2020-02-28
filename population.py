"""Groups population into LSOA2011 geographies

Data from ONS at LSOA2011 for 2001 Census, 2002-2010, 2001 Census, 2012-2017
"""

import os

import pandas as pd
import numpy as np

__author__ = "Theo Rashid"
__email__ = "tar15@ic.ac.uk"

# NUMBER OF LSOAs IN ENGLAND AND WALES IN 2011 : 34,753

# add each male and female population dataset to each list. Merge and export at the end
males_dfs = []
females_dfs = []

# 2002-2011 is split into 4 files grouped in age by year
males_2002_2011_prep_dfs = []
females_2002_2011_prep_dfs = []

for year in range(2002, 2006+1):
    males_2002_2011_prep_dfs.append(pd.read_excel("../Data/Populations/unclean populations/pop2002-2006_lsoa2011_male.xls", sheet_name = "Mid-{0!s}".format(year),  engine = "xlrd"))
    females_2002_2011_prep_dfs.append(pd.read_excel("../Data/Populations/unclean populations/pop2002-2006_lsoa2011_female.xls", sheet_name = "Mid-{0!s}".format(year),  engine = "xlrd"))
for year in range(2007, 2011+1):
    males_2002_2011_prep_dfs.append(pd.read_excel("../Data/Populations/unclean populations/pop2007-2010_lsoa2011_male.xls", sheet_name = "Mid-{0!s}".format(year),  engine = "xlrd"))
    females_2002_2011_prep_dfs.append(pd.read_excel("../Data/Populations/unclean populations/pop2007-2010_lsoa2011_female.xls", sheet_name = "Mid-{0!s}".format(year),  engine = "xlrd"))

def clean_pop_2002_2011(df, gender):
    """Function to clean dataframes from 2002 - 2011 format

    Keyword arguments:
    df -- population dataframe
    gender -- male ("m") or female ("f")
    """

    offset = 4 # first 4 rows do not contain information about group per age

    # Need a 0 age bin, and a 1-4 age bin
    df[gender + "00"] = df.iloc[:,0+offset]
    df[gender + "1_4"] = df.iloc[:, 1+offset:4+offset+1].sum(axis=1)
    lower = 5 # First 5 year age bin is 5-9
    upper = 9 # 5 year age groups
    while upper < 85:
        df[gender + str(lower) + "_" + str(upper)] = df.iloc[:, lower+offset:upper+offset+1].sum(axis=1)
        lower += 5
        upper += 5
    df[gender + "85+"] = df.iloc[:, 85+offset:90+offset+1].sum(axis=1) # separate for 85+ column
    df = df.drop(df.iloc[:,1:95], axis = 1)
    df = df.rename(columns={"LSOA11CD": "LSOA2011", gender + "00": gender + "0"})
    return df

for i in range(len(range(2002, 2011+1))):
    male_df   = clean_pop_2002_2011(males_2002_2011_prep_dfs[i], "m")
    males_dfs.append(male_df)
    female_df = clean_pop_2002_2011(females_2002_2011_prep_dfs[i], "f")
    females_dfs.append(female_df)

# Files between 2012-2017 are of the same file type with a different sheet for males and females and a population estimate for each age until 90+
for year in range(2012, 2017+1):
    males_df = pd.read_excel("../Data/Populations/unclean populations/pop{0!s}_lsoa2011.xls".format(year), sheet_name = "Mid-{0!s} Males".format(year),  engine = "xlrd", skiprows = 4)
    males_df = males_df.dropna(subset=["Unnamed: 2"])
    males_df = males_df.rename(columns={"Area Codes": "LSOA2011"})
    females_df = pd.read_excel("../Data/Populations/unclean populations/pop{0!s}_lsoa2011.xls".format(year), sheet_name = "Mid-{0!s} Females".format(year),  engine = "xlrd", skiprows = 4)
    females_df = females_df.dropna(subset=["Unnamed: 2"])
    females_df = females_df.rename(columns={"Area Codes": "LSOA2011"})

    # Sum into five year age groups (and 0, 1-4, 85+)
    age_groups_list = np.array_split(range(85), 17)[1:] # splits into groups of 5 years from 5 to 85

    males_df["m0"] = males_df.loc[:, [0]].sum(axis=1)
    males_df["m1_4"] = males_df.loc[:, [1, 2, 3, 4]].sum(axis=1)
    for group in age_groups_list:
        males_df["m" + str(min(group)) + "_" + str(max(group))] = males_df.loc[:, group].sum(axis=1)
    males_df["m85+"] = males_df.loc[:, [85, 86, 87, 88, 89, "90+"]].sum(axis=1) # separate for 85+ column
    males_df.drop(males_df.columns[1:95], axis=1, inplace=True) # Keep only the LSOA code and summed columns
    males_dfs.append(males_df)

    females_df["f0"] = females_df.loc[:, [0]].sum(axis=1)
    females_df["f1_4"] = females_df.loc[:, [1, 2, 3, 4]].sum(axis=1)
    for group in age_groups_list:
        females_df["f" + str(min(group)) + "_" + str(max(group))] = females_df.loc[:, group].sum(axis=1)
    females_df["f85+"] = females_df.loc[:, [85, 86, 87, 88, 89, "90+"]].sum(axis=1) # separate for 85+ column
    females_df.drop(females_df.columns[1:95], axis=1, inplace=True) # Keep only the LSOA code and summed columns
    females_dfs.append(females_df)

# IGNORE 2001 some LSOA2011 start at 0 population
populations_dfs = [males_dfs[i].merge(females_dfs[i], on = "LSOA2011") for i in range(len(range(2002, 2017+1)))]

# for i, df in enumerate(populations_dfs):
#     df.to_csv("pop_lsoa2011_" + str(2002 + i) + ".csv")