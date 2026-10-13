# Small screen

The combinatorial E3 ligase screen: 14 knockout genes and two control guides,
delivered in combination. This is the experiment behind the paper's claim that
genetic interactions are more common within the knockout modules than between
them, and the data the prediction model is judged on.

A separate experiment from the 1,130-gene screen in `../large_screen/`, sharing
its module definitions but not its data, its cell counts or its guide set.

Ported from `ComboData_v2/Src_v2` in the E3 ligase analysis tree.

## The notebooks

Run in order; each reads what the previous one wrote.

| # | Notebook | Kernel | Produces |
|---|---|---|---|
| 01 | `01_generate_anndata` | Python | `ANNDATA_RAW` from the 10x matrices and the CRISPR feature barcodes |
| 02 | `02_upstream_qc` | Python | guide calls attached, cells filtered, back into `ANNDATA_RAW` |
| 03 | `03_downstream_qc` | Python | `ANNDATA_PROCESSED` — normalised, HVG, PCA, neighbours, leiden |
| 04 | `04_label_transfer_leiden_clusters` | Python | `ANNDATA_LEIDEN_TC_TRANSFERRED`, and the regressed-out variant |
| 05 | `05_PrepareTrainingTestDataForBigScreen` | Python | `ANNDATA_BIG_COMBO`, the two screens combined for ComBVAE |
| 06 | `06_fit_linear_model` | Python | interaction and total-effect coefficients, under `TextFiles/` |
| 07 | `07_generate_beta_matrix` | R | gene-module and gene-program beta matrices |

Notebook 04 transfers the large screen's leiden cell-state labels onto these
cells, and 05 builds a training set spanning both, so those two read the large
screen's objects as well as this screen's.

## Paths

Nothing here points outside this repository.

| | |
|---|---|
| `paths.py`, `paths.R` | `SCREEN_DATA`, `LARGE_SCREEN_DATA` and `REFERENCE` |
| `config.py` | every file name, threshold and the guide definitions |
| `<repo>/data/small_screen/` | this screen's data, written by the notebooks here |
| `<repo>/data/large_screen/` | the objects 04 and 05 read from the other screen |
| `../large_screen/reference/` | the module tables, committed, shared by both screens |

`SCREEN_DATA` defaults to `<repo>/data/small_screen` and the environment
variable `PERTURBDECODE_SMALL_DATA` overrides it. See `data/README.md`.

## Notes on the port

**One path was wrong.** The original `config.py` looked for the large screen's
object under `outputs/anndata/OriginalFiles/`, where it does not exist; it sits
in `outputs/anndata/`, which is also where `build_anndata` writes it. Notebook
04 reads it, so that was corrected here.

**The module tables are not duplicated.** `Leiden_top100Markers.csv`,
`ME_GuideModules_leiden_6_Modules.csv` and `ME_GeneModules_leiden_11_Modules.csv`
are already committed under `../large_screen/reference/`, and `config.py` reads
them from there.

**Outputs are stripped at commit**, unlike the manuscript figure notebooks.
These are a pipeline rather than a figure record, and `03_downstream_qc` alone
is 18 MB with its outputs.

**Not ported.** `ComboData_v2/Src/` is an earlier version of this pipeline,
thirty-odd notebooks with several `-Copy1` duplicates, superseded by the seven
here. The `ComBVAE/`, `GEARS/` and `Gumbel_Softmax_VAE/` folders beside it hold
model training code rather than screen analysis.
