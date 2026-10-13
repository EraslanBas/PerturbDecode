# Where this screen's data lives. Same definition as paths.py, for the R
# notebooks.
#
# SCREEN_DATA defaults to <repo>/data/large_screen. Override it with the
# environment variable PERTURBDECODE_DATA, or make that directory a symlink to
# the tree you already have.

.findRepoRoot <- function(start = getwd()) {
    d <- normalizePath(start, mustWork = TRUE)
    while (!file.exists(file.path(d, "pyproject.toml"))) {
        parent <- dirname(d)
        if (identical(parent, d)) stop("could not locate the PerturbDecode repository root")
        d <- parent
    }
    d
}

.repoRoot <- .findRepoRoot()

SCREEN_DATA <- Sys.getenv("PERTURBDECODE_DATA")
if (!nzchar(SCREEN_DATA)) SCREEN_DATA <- file.path(.repoRoot, "data", "large_screen")

# Committed reference tables, small enough to live in the repository.
REFERENCE <- file.path(.repoRoot, "notebooks", "large_screen", "reference")

# Reference tables that build_anndata both reads and writes.
TEXTFILES <- file.path(.repoRoot, "notebooks", "large_screen", "build_anndata", "TextFiles")

screenPath    <- function(...) file.path(SCREEN_DATA, ...)
referencePath <- function(...) file.path(REFERENCE, ...)
textfilesPath <- function(...) file.path(TEXTFILES, ...)
