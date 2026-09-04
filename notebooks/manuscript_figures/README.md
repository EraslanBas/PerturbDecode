# Manuscript figure notebooks

The notebooks that produced the figures in Geiger-Schuller, Eraslan et al.,
*Systematically characterizing the roles of E3-ligase family members in
inflammatory responses with massively parallel Perturb-seq*, bioRxiv 2023,
[doi:10.1101/2023.01.23.525198](https://doi.org/10.1101/2023.01.23.525198).

They are kept here as a **methods record**: the code behind each published
panel, in the state it was run. They are not part of the PerturbDecode package,
are not installed by `pip install PerturbDecode`, and are not maintained against
the current API. They come from
[PerturbDecode_v1](https://github.com/EraslanBas/PerturbDecode_v1), which
predates the package.

For the current, supported pipeline see the
[tutorials](https://perturbdecode.readthedocs.io/en/latest/tutorials/index.html).

## What each notebook produces

| Notebook | Kernel | Panels |
|---|---|---|
| `00_LPSPlusMinusAnalysis.ipynb` | Python | LPS +/- comparison underlying Figure 1 |
| `Figure1_CDEFGH.ipynb` | Python | Figure 1C-H |
| `Figure1_I-GeneLevel.ipynb` | Python | Figure 1I, gene level |
| `Figure2_ABC.ipynb` | Python | Figure 2A-C |
| `Figure2_D.ipynb` | R | Figure 2D |
| `Figure3_A.ipynb` | R | Figure 3A, Supp. 1H |
| `Figure3_B.ipynb` | Python | Figure 3B |
| `Figure3_CD.ipynb` | Python | Figure 3C, 3D |
| `Figure3_E.ipynb` | R | Figure 3E, Supp. 4D, 4E |
| `Figure3_F.ipynb` | R | Figure 3F |
| `Figure4_A.ipynb` | R | Figure 4A |
| `Figure4_BCEFHI.ipynb` | Python | Figure 4B, C, E, F, H, I |
| `Figure4_BEH.ipynb` | R | Figure 4B, E, H |
| `Figure5_C.ipynb` | R | Figure 5C |
| `Figure5_DE.ipynb` | R | Figure 5D, 5E, Supp. 6C |
| `Figure5_F.ipynb` | R | Figure 5F, Supp. 7D, 7E |
| `Figure5_G.ipynb` | R | Figure 5G, Supp. 6O, 6P, 7F |
| `SuppFigure1_F.ipynb` | R | Supp. 1F |
| `SuppFigure1_G.ipynb` | R | Supp. 3A, 3B |
| `SuppFigure1_HZ.ipynb` | Python | Supp. 1H-Z |
| `SuppFigure_2AB.ipynb` | Python | Supp. 2A, 2B |
| `SuppFigure_2Z.ipynb` | R | Supp. 2Z |
| `SuppFigure_5CD.ipynb` | R | Supp. 5C, 5D |
| `SuppFigure_5E.ipynb` | R | Supp. 5E |

Nine notebooks run on the IPython kernel (several calling into R through
`rpy2`'s `%%R` magic) and fifteen on the IRkernel. `Main.R`, `Conf.R`,
`Utilities.R`, `libraries.py` and `parameters.py` are the shared setup they
source.

## Why they are not executable as committed

The notebooks are committed **without outputs**, and they cannot be re-run from
this repository, for two reasons.

**The data is not here and is not distributable.** They read the intermediate
results of the full E3 ligase screen: effect-size matrices, gene and guide
module assignments, combinatorial-perturbation RDS files, and `.h5ad` objects
that run to tens of gigabytes each. None of that is in this repository, and the
assembled screen is available from
[GEO GSE327057](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE327057)
rather than from here.

**The paths they use are those of the original analysis tree.** Every notebook
reads relative paths such as `./../TextFiles/`, `./../MixedEffectLMOutputs/` and
`./../Notebooks/CombinatorialPerturbations/RDSFiles/`, and the Python ones
`os.chdir(projectDir)` into an absolute path set in `parameters.py`. Those
locations describe the analysis directory as it stood in 2023; reproducing a
figure means pointing them at your own copy of the corresponding inputs.

`Conf.R` still carries the absolute paths of the machine the analysis was
originally run on, which no longer exist.

## Dependencies

Beyond the PerturbDecode dependencies these notebooks need the `[r]` extra, an
IRkernel, and the R packages sourced by `Main.R`: `pheatmap`, `corrplot`,
`ggplot2`, `cowplot`, `RColorBrewer`, `pls`, `data.table`, `reshape2`,
`factoextra`, `maptree`, `ggpubr`, `ica`, `ICtest`, `repr`, `plyr`.
