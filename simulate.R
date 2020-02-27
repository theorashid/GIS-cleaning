
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
    pivot_wider(names_from = "age_group", values_from = "population")

populations <- data.matrix(pop_IMD_df_wide[9:26])
income_dep <- data.matrix(pop_IMD_df_wide[5]) # max 0.1852

# Rough estimated death rates for 18 age groups
mxE <- exp(-5.5 + c(-1,-3,-2.9,-1.8,-1.7,-1.7,-1.6,-1.4,-.8,-.2,.3,1.0,1.5,1.9,2.4,2.8,3.4,3.8)) # mean 0.0273, sd 0.0502
mxE_mat <- t(replicate(135380, mxE)) # expand this into the length of populations/income deprivation

# Add a term proportional to income deprivation
mxE_mat <- mxE_mat + matrix(rep(income_dep, 18), ncol=18) * 0.3

# Add some random normal noise
noise <- matrix(rnorm(2436840), 135380) * 0.001
mxE_mat <- mxE_mat + noise
mxE_mat[mxE_mat < 0] <- 0 # cannot have negative death rates

# Populations
deaths <- matrix(, nrow = 135380, ncol = 18)
for (i in 1:135380) {
    pop <- populations[i,]
    m   <- mxE_mat[i,]
    deaths[i,] <- rpois(n=18, m*pop)
}

# Flatten # as.vector(t(deaths)) # reads across rows
# Add as column
# write to csv
# Get only Hammersmith and Fulham for unit test
# write to csv