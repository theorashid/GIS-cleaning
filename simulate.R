
# Theo AO Rashid -- February 2020

# ----- Simulate death data -----
# Build model from the death rates and add a term proportional
# to LSOA's income deprivation. This should have some spatial
# component. Add some random noise also

library(dplyr)
library(tidyr)

set.seed(1)

# Import the data
pop_IMD_df <- read.csv(file = "../Data/pop_IMD_2004_17.csv") %>%
    select(-X)

# Reshape with column for each age group
pop_IMD_df_wide <- pop_IMD_df %>%
    select("LAD2011", "MSOA2011", "LSOA2011", "YEAR", "age_group", "sex", "population", "IMD.score", "income.score", "employment.score") %>% # drop rank cols
    pivot_wider(names_from = "age_group", values_from = "population")

populations <- data.matrix(pop_IMD_df_wide[9:27]) # dim (135380, 19)
income_dep <- data.matrix(pop_IMD_df_wide[7]) # mean 0.1852

# Rough estimated death rates for 19 age groups
mxE <- exp(-5.5 + c(0,-2.9,-3,-2.9,-1.8,-1.7,-1.7,-1.6,-1.4,-.8,-.2,.3,1.0,1.5,1.9,2.4,2.8,3.4,3.8)) # mean 0.0260, sd 0.0491
mxE_mat <- t(replicate(135380, mxE)) # expand this into the length of populations/income deprivation

# Add a term proportional to income deprivation
mxE_mat <- mxE_mat + matrix(rep(income_dep, 19), ncol=19) * 0.3

# Add some random normal noise
noise <- matrix(rnorm(2572220), 135380) * 0.001
mxE_mat <- mxE_mat + noise
mxE_mat[mxE_mat < 0] <- 0 # cannot have negative death rates

# Populations
deaths <- matrix(, nrow = 135380, ncol = 19)
for (i in 1:135380) {
    pop <- populations[i,]
    m   <- mxE_mat[i,]
    deaths[i,] <- rpois(n=19, m*pop)
}

pop_IMD_df$deaths = as.vector(t(deaths)) # Flatten, reads across rows
pop_IMD_df <- pop_IMD_df[, c(1,2,3,4,5,6,16,7,8,9,10,11,12,13,14,15)]

# pop_IMD_df.to_csv("mortsim.csv")

# Get only Hammersmith and Fulham for unit test
pop_IMD_df_hf <- read.csv(file = "../Data/pop_IMD_2004_17_hf.csv") %>%
    select(-X, -index)
deaths_hf <- pop_IMD_df %>%
    filter(LAD2011 == "E09000013") %>%
    select(LSOA2011, YEAR, age_group, sex, deaths)

# pop_IMD_df_hf.to_csv("mortsim_hf.csv")