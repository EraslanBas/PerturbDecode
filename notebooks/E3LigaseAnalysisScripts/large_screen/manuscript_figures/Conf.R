# Paths for the R figure notebooks.
#
# Nothing here points outside this repository. SCREEN_DATA is the screen's data
# root, resolved by ../paths.R -- <repo>/data/large_screen unless
# PERTURBDECODE_DATA says otherwise. See data/README.md.

source("../paths.R")

dataDir   <- screenPath("outputs", "anndata")
davidDir  <- screenPath("outputs", "DAVID_queries")
rDir      <- screenPath("R")
rdsDir    <- screenPath("R", "RDSFiles")

# Outputs are written beside these notebooks.
projectDir <- normalizePath(".", mustWork = FALSE)
