"""Smaller unit test dataset using one LAD

LAD is Hammersmith and Fulham (E09000013)
"""

import os

import pandas as pd
import numpy as np
import geopandas as gpd
import matplotlib.pyplot as plt

__author__ = "Theo Rashid"
__email__ = "tar15@ic.ac.uk"

# IMPORT LONDON DATA
# Population and IMD data
pop_IMD_df = pd.read_csv("../Data/pop_IMD_2004_17.csv", engine = "python", index_col=0)

# Lookup table
ldn_lookup = pd.read_csv("../Data/ldn_geog_lookup.csv", engine = "python")

# # shape data
# lsoa_shp = gpd.read_file("../Data/ldn_LSOA2011_shape/LSOA11_LDN.shp")
# # lsoa_shp.plot()
# # plt.show()

# REDUCE TO HAMMERSMITH AND FULHAM ONLY
hf_pop_IMD_df = pop_IMD_df[pop_IMD_df["LAD2011"] == "E09000013"]
hf_lookup     = ldn_lookup[ldn_lookup["LAD2011"] == "E09000013"]
# hf_shp        = lsoa_shp[lsoa_shp["LSOA11"].isin(hf_lookup["LSOA2011"])]

# hf_pop_IMD_df.to_csv("pop_IMD_2004_17_hf.csv")
# hf_lookup.to_csv("hf_geog_lookup.csv")
