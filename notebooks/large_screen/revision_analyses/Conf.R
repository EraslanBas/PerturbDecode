# Paths for the R revision notebooks.
#
# The original Conf.R here pointed at /home/beraslan/jovian-work, a machine
# that no longer exists; dataDir and davidDir were dead and nothing read them.
# Everything now resolves through ../paths.R.

source("../paths.R")   # SCREEN_DATA, REFERENCE, TEXTFILES

# Written by build_anndata/18_BuildCombinedKOObject.
# It sits under OriginalFiles/, not outputs/anndata/ as the notebooks assumed.
ANNDATA_ALL_KO <- screenPath("outputs", "anndata", "OriginalFiles",
                             "adata-hash-features_ALLKO_ForSCVI_09072021.h5ad")

# Outputs are written beside these notebooks.
projectDir <- normalizePath(".", mustWork = FALSE)
