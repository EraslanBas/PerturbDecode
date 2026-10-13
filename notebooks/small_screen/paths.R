# Where this screen's data lives. Same definition as paths.py, for the R
# notebooks. See that file for the full note.

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

SCREEN_DATA <- Sys.getenv("PERTURBDECODE_SMALL_DATA")
if (!nzchar(SCREEN_DATA)) SCREEN_DATA <- file.path(.repoRoot, "data", "small_screen")

LARGE_SCREEN_DATA <- Sys.getenv("PERTURBDECODE_DATA")
if (!nzchar(LARGE_SCREEN_DATA)) LARGE_SCREEN_DATA <- file.path(.repoRoot, "data", "large_screen")

# Committed reference tables, shared with the large screen.
REFERENCE <- file.path(.repoRoot, "notebooks", "large_screen", "reference")

screenPath      <- function(...) file.path(SCREEN_DATA, ...)
largeScreenPath <- function(...) file.path(LARGE_SCREEN_DATA, ...)
referencePath   <- function(...) file.path(REFERENCE, ...)
