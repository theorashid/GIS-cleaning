import os
import pandas as pd
import numpy as np

# Files between 2012-2017 are of the same file type
# for year in np.arange(2012, 2017+1):
# use placeholders
males_df = pd.read_excel("../Data/Populations/pop2012_lsoa2011.xls", sheet_name = "Mid-2012 Males",  engine = 'xlrd', skiprows = 4)
males_df = males_df.dropna(subset=["Unnamed: 2"])

# Sum into five year age groups (and 85+)
age_groups_list = np.array_split(range(85), 17)
for group in age_groups_list:
    males_df["m" + str(min(group)) + "_" + str(max(group))] = males_df.loc[:, group].sum(axis=1)
males_df["m85+"] = males_df.loc[:, [85, 86, 87, 88, 89, "90+"]].sum(axis=1)

males_df.drop(males_df.columns[1:95], axis=1, inplace=True) # Keep only the LSOA code and summed columns