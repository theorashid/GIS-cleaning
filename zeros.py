"""Discrepancy between LSOA2001 and LSOA2011

Some LSOA2011 do not exist in 2001
There was no postcode in these areas in 2001 as nobody lived there
Check whether the data between these two points match these observations (true zeros)
OR they LSOA2011 geographies have been forced to fit the contraint of populations 1000-3000
"""

import os

import pandas as pd
import numpy as np
from dbfread import DBF
import matplotlib.pyplot as plt

__author__ = "Theo Rashid"
__email__ = "tar15@ic.ac.uk"

# NUMBER OF LSOAs IN ENGLAND AND WALES IN 2011 : 34,753

# add each male and female population dataset to each list. Merge and export at the end
males_dfs = []
females_dfs = []

# 2001 census populations are grouped by 5 year age group but at COA level
# Need to group by LSOA level
pop_2001_df = pd.read_csv("../Data/Populations/pop2001_coa11.csv", engine = "python")
geog_2011 = pd.read_csv("../Data/Geography/OA2011_lookup.csv", engine = "python")
geog_2011 = geog_2011[~geog_2011["LSOA11CD"].astype(str).str.startswith('S')] # Remove scottish geographies
pop_2001_df = pop_2001_df.merge(geog_2011, left_on="coa11", right_on="OA11CD").groupby("LSOA11CD").sum().reset_index()

# DISCREPANCY BETWEEN 2001 and 2011 OA/LSOA numbers

# LSOA2011 in geog_2011 but not in pop_2001_df
missing_geog = geog_2011["LSOA11CD"][~geog_2011["LSOA11CD"].isin(pop_2001_df["LSOA11CD"])].dropna().unique()

# PLOT MISSING GEOG POPULATIONS FOR ALL 2002-2011
# SEE IF RISE OR ALWAYS BETWEEN 1000-3000 thresholds

# 2002-2011 is split into 4 files grouped in age by year
m_2002_11_dfs = []
f_2002_11_dfs = []
for year in range(2002, 2006+1):
    m_2002_11_dfs.append(pd.read_excel("../Data/Populations/pop2002-2006_lsoa2011_male.xls", sheet_name = "Mid-{0!s}".format(year),  engine = "xlrd"))
    f_2002_11_dfs.append(pd.read_excel("../Data/Populations/pop2002-2006_lsoa2011_female.xls", sheet_name = "Mid-{0!s}".format(year),  engine = "xlrd"))
for year in range(2007, 2010+1):
    m_2002_11_dfs.append(pd.read_excel("../Data/Populations/pop2007-2010_lsoa2011_male.xls", sheet_name = "Mid-{0!s}".format(year),  engine = "xlrd"))
    f_2002_11_dfs.append(pd.read_excel("../Data/Populations/pop2007-2010_lsoa2011_female.xls", sheet_name = "Mid-{0!s}".format(year),  engine = "xlrd"))

for df in m_2002_11_dfs:
    new_df = df[["LSOA11CD", "all_ages"]]
    new_df = new_df.rename(columns={"LSOA11CD": "LSOA2011", "all_ages": "All Ages"})
    males_dfs.append(new_df)

for df in f_2002_11_dfs:
    new_df = df[["LSOA11CD", "all_ages"]]
    new_df = new_df.rename(columns={"LSOA11CD": "LSOA2011", "all_ages": "All Ages"})
    females_dfs.append(new_df)

# 2011 census populations
males_df_2011 = pd.read_excel("../Data/Populations/pop2011_lsoa2011.xls", sheet_name = "Mid-2011 Males",  engine = "xlrd", skiprows = 3).dropna(subset=["Unnamed: 2"])
females_df_2011 = pd.read_excel("../Data/Populations/pop2011_lsoa2011.xls", sheet_name = "Mid-2011 Females",  engine = "xlrd", skiprows = 3).dropna(subset=["Unnamed: 2"])

males_df_2011 = males_df_2011[["Area Codes", "All Ages"]]
males_df_2011 = males_df_2011.rename(columns={"Area Codes": "LSOA2011"})

females_df_2011 = females_df_2011[["Area Codes", "All Ages"]]
females_df_2011 = females_df_2011.rename(columns={"Area Codes": "LSOA2011"})

males_dfs.append(males_df_2011)
females_dfs.append(females_df_2011)

# # Merge male and female to get total population
populations_dfs = [males_dfs[i].merge(females_dfs[i], on = "LSOA2011") for i in range(len(range(2002, 2011+1)))]
for df in populations_dfs:
    df["pop"] = df["All Ages_x"] + df["All Ages_y"]
    df = df.drop(["All Ages_x", "All Ages_y"], axis=1, inplace=True)

# MISSING GEOG PLOT POP vs YEAR
    
years = np.arange(2002, 2011+1)
# need an array for each dataset
population_trends = []
for LSOA in missing_geog:
    tmp = []
    for df in populations_dfs:
        short = df[df["LSOA2011"] == LSOA]
        population = short["pop"].values[0]
        tmp.append(population)
    population_trends.append(tmp)

# style
plt.style.use('seaborn-darkgrid')
palette = plt.get_cmap('Set1')

for i, trend in enumerate(population_trends):
    plt.plot(years, trend, color=palette(i), linewidth=0.5, alpha=0.8)
plt.title("Missing geographies (2001) populations")
plt.xlabel("Year")
plt.ylabel("Population")

plt.show()

# THE POPULATIONS START FROM ZERO