# R example
#
# Example of using the package from R
#

# Source the R functions
source("../R/functions.R")

# Use an R function
result <- example_r_function(5)
print(paste("Result:", result))

# Example of calling Python from R using reticulate
# Uncomment if you have reticulate installed
# library(reticulate)
# py <- import("perturbdecode")
# # Call Python functions here
