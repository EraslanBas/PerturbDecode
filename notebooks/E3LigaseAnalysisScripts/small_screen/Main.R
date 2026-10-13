# Main.R — package loader for the ComboData_v2 R notebooks.
# Sourced from the analysis notebooks together with Utilities.R.

suppressPackageStartupMessages({
  library(pheatmap)     # heatmaps
  library(ggplot2)      # plotting
  library(ggpubr)       # stat_compare_means(), publication-ready plots
  library(data.table)   # copy(), fast frames
})
