# Utilities.R — shared annotation colors and small helpers used by the
# ComboData_v2 R notebooks. Sourced together with Main.R.

# ---------------------------------------------------------------------------
# Annotation color palettes for pheatmap
# ---------------------------------------------------------------------------
annoCols <- list(
  GeneGroup = c(
    G0 = "#A6CEE3", G1  = "#1F78B4", G2  = "#B2DF8A", G3  = "#33A02C",
    G4 = "#FB9A99", G5  = "#FDBF6F", G6  = "#FF7F00", G7  = "#CAB2D6",
    G8 = "#6A3D9A", G9  = "#FFFF99", G10 = "#B5651D", G11 = "black"
  ),
  GuideGroup = c(
    M1 = "#aa40fc", M2 = "#1f77b4", M3 = "#ff7f0e",
    M4 = "#8c564b", M5 = "#d62728", M6 = "#279e68"
  ),
  NewGeneGroup = c(
    GP_1  = "#FF7F00", GP_2  = "#FFFF99", GP_3  = "#B5651D", GP_4  = "#FDBF6F",
    GP_5  = "#FB9A99", GP_6  = "#CAB2D6", GP_7  = "#A6CEE3", GP_8  = "#1F78B4",
    GP_9  = "#33A02C", GP_10 = "#B2DF8A", GP_11 = "#6A3D9A"
  ),
  NewGeneAllGroups = c(
    GP_1  = "#FF7F00", GP_2  = "#FFFF99", GP_3  = "#B5651D", GP_4  = "#FDBF6F",
    GP_5  = "#FB9A99", GP_6  = "#CAB2D6", GP_7  = "#A6CEE3", GP_8  = "#1F78B4",
    GP_9  = "#33A02C", GP_10 = "#B2DF8A", GP_11 = "#6A3D9A",
    GPC_1 = "blue",    GPC_2 = "magenta", GPC_3 = "cyan",
    GPC_4 = "orange",  GPC_5 = "red"
  ),
  NewPrograms = c(
    GPC_1 = "blue", GPC_2 = "magenta", GPC_3 = "cyan",
    GPC_4 = "orange", GPC_5 = "red"
  ),
  GuideGroupCombo = c(
    M3_M3 = "blue", M3_M5 = "green", M5_M5 = "red"
  )
)

# ---------------------------------------------------------------------------
# Operators
# ---------------------------------------------------------------------------
`%ni%` <- Negate(`%in%`)

# ---------------------------------------------------------------------------
# Math / stats helpers
# ---------------------------------------------------------------------------
computeR2 <- function(response, prediction) {
  rss <- sum((response - prediction)^2, na.rm = TRUE)
  tss <- sum((response - mean(response, na.rm = TRUE))^2)
  1 - rss / tss
}

getOutliers <- function(x) {
  qX <- quantile(x)
  IQR <- qX[4] - qX[2]
  x[x < qX[2] - 1.5 * IQR | x > qX[4] + 1.5 * IQR]
}

getExtremeOutliers <- function(x) {
  qX <- quantile(x)
  IQR <- qX[4] - qX[2]
  x[x < qX[2] - 3 * IQR | x > qX[4] + 3 * IQR]
}

n_fun <- function(x) {
  data.frame(y = median(x), label = paste0("n = ", length(x)))
}

getJaccardDistanceMatrix <- function(inList) {
  n <- length(inList)
  m <- matrix(0, nrow = n, ncol = n,
              dimnames = list(names(inList), names(inList)))
  for (i in seq_len(n)) {
    for (j in i:n) {
      jacc <- length(intersect(inList[[i]], inList[[j]])) /
              length(union(inList[[i]], inList[[j]]))
      m[i, j] <- jacc
      m[j, i] <- jacc
    }
  }
  as.data.frame(m)
}

# ---------------------------------------------------------------------------
# I/O helpers
# ---------------------------------------------------------------------------
save_pheatmap_pdf <- function(x, filename, width = 7, height = 7) {
  stopifnot(!missing(x), !missing(filename))
  pdf(filename, width = width, height = height)
  grid::grid.newpage()
  grid::grid.draw(x$gtable)
  dev.off()
}

writePathwayFile <- function(pathwayGenes, fileName, cNames = FALSE) {
  maxlen <- max(lengths(pathwayGenes))
  padded <- lapply(pathwayGenes, function(lst) c(lst, rep(NA, maxlen - length(lst))))
  df <- do.call("cbind", lapply(padded, as.data.frame))
  colnames(df) <- names(pathwayGenes)
  write.table(df, fileName, sep = ",", row.names = FALSE,
              na = " ", quote = FALSE, col.names = cNames)
}
