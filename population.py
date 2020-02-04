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

# # 2001 census populations are grouped by 5 year age group but at COA level
# # Need to group by LSOA level
# pop_2001_df = pd.read_csv("../Data/Populations/pop2001_coa11.csv", engine = "python")
# geog_2011 = pd.read_csv("../Data/Geography/OA2011_lookup.csv", engine = "python")
# geog_2011 = geog_2011[~geog_2011["LSOA11CD"].astype(str).str.startswith('S')] # Remove scottish geographies
# pop_2001_df = pop_2001_df.merge(geog_2011, left_on="coa11", right_on="OA11CD").groupby("LSOA11CD").sum()
# # DISCREPANCY BETWEEN 2001 and 2011 OA/LSOA numbers

# 2002-2011 is split into 4 files grouped in age by year
males_2002_2010_prep_dfs = []
females_2002_2010_prep_dfs = []

for year in range(2002, 2006+1):
    males_2002_2010_prep_dfs.append(pd.read_excel("../Data/Populations/pop2002-2006_lsoa2011_male.xls", sheet_name = "Mid-{0!s}".format(year),  engine = "xlrd"))
    females_2002_2010_prep_dfs.append(pd.read_excel("../Data/Populations/pop2002-2006_lsoa2011_female.xls", sheet_name = "Mid-{0!s}".format(year),  engine = "xlrd"))
for year in range(2007, 2010+1):
    males_2002_2010_prep_dfs.append(pd.read_excel("../Data/Populations/pop2007-2010_lsoa2011_male.xls", sheet_name = "Mid-{0!s}".format(year),  engine = "xlrd"))
    females_2002_2010_prep_dfs.append(pd.read_excel("../Data/Populations/pop2007-2010_lsoa2011_female.xls", sheet_name = "Mid-{0!s}".format(year),  engine = "xlrd"))

def clean_pop_2002_2010(df, gender):
    """Function to clean dataframes from 2002 - 2011 format

    Keyword arguments:
    df -- population dataframe
    gender -- male ("m") or female ("f")
    """

    offset = 4 # first 4 rows do not contain information about group per age

    lower = 0
    upper = 4 # 5 year age groups
    while upper < 85:
        df[gender + str(lower) + "_" + str(upper)] = df.iloc[:, lower+offset:upper+offset+1].sum(axis=1)
        lower += 5
        upper += 5
    df[gender + "85+"] = df.iloc[:, 85+offset:90+offset+1].sum(axis=1) # separate for 85+ column
    df = df.drop(df.iloc[:,1:95], axis = 1)
    df = df.rename(columns={"LSOA11CD": "LSOA2011"})
    return df

for i in range(len(range(2002, 2010+1))):
    male_df   = clean_pop_2002_2010(males_2002_2010_prep_dfs[i], "m")
    males_dfs.append(male_df)
    female_df = clean_pop_2002_2010(females_2002_2010_prep_dfs[i], "f")
    females_dfs.append(female_df)

# 2011 census populations are grouped by 5 year age group but the 90+ needs to be changed to 85+
males_df_2011 = pd.read_excel("../Data/Populations/pop2011_lsoa2011.xls", sheet_name = "Mid-2011 Males",  engine = "xlrd", skiprows = 3).dropna(subset=["Unnamed: 2"])
females_df_2011 = pd.read_excel("../Data/Populations/pop2011_lsoa2011.xls", sheet_name = "Mid-2011 Females",  engine = "xlrd", skiprows = 3).dropna(subset=["Unnamed: 2"])

area_codes = males_df_2011["Area Codes"]

males_df_2011["85+"] = males_df_2011.iloc[:,-2] + males_df_2011.iloc[:,-1]
males_df_2011 = males_df_2011.drop(columns=["Area Codes", "Area Names", "Unnamed: 2", "All Ages", "85-89", "90+"])
males_df_2011 = males_df_2011.add_prefix('m')
males_df_2011.columns = males_df_2011.columns.str.replace("-", "_")
males_df_2011.insert(0, "LSOA 2011", area_codes)
males_dfs.append(males_df_2011)

females_df_2011["85+"] = females_df_2011.iloc[:,-2] + females_df_2011.iloc[:,-1]
females_df_2011 = females_df_2011.drop(columns=["Area Codes", "Area Names", "Unnamed: 2", "All Ages", "85-89", "90+"])
females_df_2011 = females_df_2011.add_prefix('f')
females_df_2011.columns = females_df_2011.columns.str.replace("-", "_")
females_df_2011.insert(0, "LSOA2011", area_codes)
females_dfs.append(females_df_2011)

# Files between 2012-2017 are of the same file type with a different sheet for males and females and a population estimate for each age until 90+
for year in range(2012, 2017+1):
    males_df = pd.read_excel("../Data/Populations/pop{0!s}_lsoa2011.xls".format(year), sheet_name = "Mid-{0!s} Males".format(year),  engine = "xlrd", skiprows = 4)
    males_df = males_df.dropna(subset=["Unnamed: 2"])
    males_df = males_df.rename(columns={"Area Codes": "LSOA2011"})
    females_df = pd.read_excel("../Data/Populations/pop{0!s}_lsoa2011.xls".format(year), sheet_name = "Mid-{0!s} Females".format(year),  engine = "xlrd", skiprows = 4)
    females_df = females_df.dropna(subset=["Unnamed: 2"])
    females_df = females_df.rename(columns={"Area Codes": "LSOA2011"})

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

populations_dfs = [males_dfs[i].merge(females_dfs[i], on = "LSOA2011") for i in range(len(range(2001+1, 2017+1)))]

# for i, df in enumerate(populations_dfs):
#     df.to_csv("pop_lsoa2011_" + str(2001+1 + i) + ".csv") # change to 2001 when census data is fixed

##### CHECK THE NUMBERS FOR CONSISTENCY
##### EXPORT EACH DATAFRAME AS CSV df.to_csv('out.csv')