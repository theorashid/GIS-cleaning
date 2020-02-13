"""Intersect Ward and postcode geographies

Using geopandas
"""

import os

import pandas as pd
import numpy as np
import geopandas as gpd
import functools
import matplotlib.pyplot as plt

__author__ = "Theo Rashid"
__email__ = "tar15@ic.ac.uk"

pc_df   = gpd.read_file("../Data/ldn_postcode_shape/Pc2011_810111.shp")
ward_df = gpd.read_file("../Data/ldn_Ward98_shape/Ward98.shp")

# Find which postcodes are in each Ward
gpd.sjoin(pc_df, ward_df, how="inner", op="intersects") # not working