"""Clean IMD data to consistent LSOA 2011 geographies

Data from ONS
"""

import os

import pandas as pd
import numpy as np
from dbfread import DBF

__author__ = "Theo Rashid"
__email__ = "tar15@ic.ac.uk"

dbf = DBF("../Data/Geography/gb_ONS_geog_intersects.dbf")
df = pd.DataFrame(iter(dbf))

# IMD is for the ENGLISH indices of deprivation
# We will get rid of any Scottish or Welsh geographies
# More specifically, as our study is only London focussed, we will get rid of outside London
# LAD11 must start with "E09"
ldn_df = df[df["lad11"].astype(str).str.startswith("E09")]

# Between 184612 postcodes, this leaves:
# - 33 LADUA2001, 33 LAD2011
# - 4765 LSOA2001, 4835 LSOA2011