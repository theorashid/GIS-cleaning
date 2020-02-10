"""Clean IMD data to consistent LSOA 2011 geographies

Data from ONS
"""

import os

import pandas as pd
import numpy as np
import functools
from dbfread import DBF

from reaggregate import reaggregator

__author__ = "Theo Rashid"
__email__ = "tar15@ic.ac.uk"

dbf = DBF("../Data/Geography/gb_ONS_geog_intersects.dbf")
df = pd.DataFrame(iter(dbf))

# IMD is for the ENGLISH indices of deprivation
# We will get rid of any Scottish or Welsh geographies
# More specifically, as our study is only London focussed, we will get rid of outside London
# LAD11 must start with "E09"
ldn_df = df[df["lad11"].astype(str).str.startswith("E09")]
ldn_df = ldn_df.drop(columns=["coa11", "msoa11", "lad11", "ed81", "coa01", "ladua01"]) # drop unnecessary geographies
ldn_df = ldn_df.rename(columns={"lsoa11": "LSOA2011", "lsoa01": "SOA2001"}) # rename LSOA for consistnecy with IMD data

# Between 184612 postcodes, this leaves:
# - 33 LADUA2001, 33 LAD2011
# - 4765 LSOA2001, 4835 LSOA2011

# We are only interested in IMD, and income/employement deprivation (proportionate)

# IMD data before 2011 comes in at ward level (2000) or LSOA2001 boundaries (2004, 2007, 2010)

# IMD 2000
sheets = []
for sheet in ["IMD", "Income", "Employment"]:
    df = pd.read_excel("../Data/IMD/IMD2000.xls", sheet_name = sheet,  engine = "xlrd")
    df = df[(df["DETR LA code"] >= 5000) & (df["DETR LA code"] < 6000)] # London only
    df = df.drop(columns=["Ward Name", "LA", "LA Name", "DETR LA code"])
    sheets.append(df)

# merge all sheets into one keeping only the scores
IMD_2000_df = functools.reduce(lambda left, right: pd.merge(left, right, on = "Ward"), sheets)
IMD_2000_df = IMD_2000_df[["Ward", "Index of Multiple Deprivation Score",
                           "Income Domain Score", "Employment Domain Score"]]
IMD_2000_df = IMD_2000_df.rename(columns={"Index of Multiple Deprivation Score": "IMD score",
                                          "Income Domain Score": "income score", "Employment Domain Score": "employment score"})
                                          
# IMD 2004
sheets = []
for sheet in ["IMD 2004", "Income", "Employment"]:
    df = pd.read_excel("../Data/IMD/IMD2004.xls", sheet_name = sheet,  engine = "xlrd")
    df = df[df["GOR CODE"] == "H"] # London only
    df = df.drop(columns=["LA CODE", "LA NAME", "GOR CODE", "GOR NAME"])
    sheets.append(df)

IMD_2004_df = functools.reduce(lambda left, right: pd.merge(left, right, on = "SOA"), sheets)
IMD_2004_df = IMD_2004_df[["SOA", "IMD SCORE", "INCOME SCORE", "EMPLOYMENT SCORE"]]
IMD_2004_df = IMD_2004_df.rename(columns={"SOA": "SOA2001", "IMD SCORE": "IMD score", "INCOME SCORE": "income score",
                                          "EMPLOYMENT SCORE": "employment score"})

IMD_2004_df = reaggregator("SOA2001", "LSOA2011", ldn_df, IMD_2004_df)

# IMD 2007
sheets = []
for sheet in ["IMD 2007", "Income", "Employment"]:
    df = pd.read_excel("../Data/IMD/IMD2007.xls", sheet_name = sheet,  engine = "xlrd")
    df = df[df["GOR CODE"] == "H"] # London only
    df = df.drop(columns=["LA CODE", "LA NAME", "GOR CODE", "GOR NAME"])
    sheets.append(df)

IMD_2007_df = functools.reduce(lambda left, right: pd.merge(left, right, on = "LSOA"), sheets)
IMD_2007_df = IMD_2007_df[["LSOA", "IMD SCORE", "INCOME SCORE", "EMPLOYMENT SCORE"]]
IMD_2007_df = IMD_2007_df.rename(columns={"LSOA": "SOA2001", "IMD SCORE": "IMD score", "INCOME SCORE": "income score",
                                          "EMPLOYMENT SCORE": "employment score"})

IMD_2007_df = reaggregator("SOA2001", "LSOA2011", ldn_df, IMD_2007_df)

# IMD 2010
IMD_2010_df = pd.read_csv("../Data/IMD/IMD2010.csv", engine = "python")
IMD_2010_df = IMD_2010_df[IMD_2010_df["GOR CODE"] == "H"] # London only
IMD_2010_df = IMD_2010_df[["LSOA CODE", "IMD SCORE", "INCOME SCORE", "EMPLOYMENT SCORE"]]
IMD_2010_df = IMD_2010_df.rename(columns={"LSOA CODE": "SOA2001", "IMD SCORE": "IMD score", "INCOME SCORE": "income score",
                                          "EMPLOYMENT SCORE": "employment score"})

IMD_2010_df = reaggregator("SOA2001", "LSOA2011", ldn_df, IMD_2010_df)

# IMD data after 2011 comes with the desired LSOA2011 boundaries

# IMD 2015
IMD_2015_df = pd.read_excel("../Data/IMD/IMD2015.xlsx", sheet_name = "ID2015 Scores",  engine = "xlrd")
IMD_2015_df = IMD_2015_df[IMD_2015_df["Local Authority District code (2013)"].astype(str).str.startswith("E09")] # London only
IMD_2015_df = IMD_2015_df[["LSOA code (2011)", "Index of Multiple Deprivation (IMD) Score", "Income Score (rate)",
                           "Employment Score (rate)"]]
IMD_2015_df = IMD_2015_df.rename(columns={"LSOA code (2011)": "LSOA2011", "Index of Multiple Deprivation (IMD) Score": "IMD score",
                                          "Income Score (rate)": "income score", "Employment Score (rate)": "employment score"})

# IMD 2019
IMD_2019_df = pd.read_excel("../Data/IMD/IMD2019.xlsx", sheet_name = "IoD2019 Scores",  engine = "xlrd")
IMD_2019_df = IMD_2019_df[IMD_2019_df["Local Authority District code (2019)"].astype(str).str.startswith("E09")] # London only
IMD_2019_df = IMD_2019_df[["LSOA code (2011)", "Index of Multiple Deprivation (IMD) Score", "Income Score (rate)",
                           "Employment Score (rate)"]]
IMD_2019_df = IMD_2019_df.rename(columns={"LSOA code (2011)": "LSOA2011", "Index of Multiple Deprivation (IMD) Score": "IMD score",
                                          "Income Score (rate)": "income score", "Employment Score (rate)": "employment score"})