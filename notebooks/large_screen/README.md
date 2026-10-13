# Large screen

The genome-scale E3 ligase Perturb-seq screen of Geiger-Schuller, Eraslan et al.,
[doi:10.1101/2023.01.23.525198](https://doi.org/10.1101/2023.01.23.525198) —
the screen the manuscript is built on, and the one every notebook below reads.

| Folder | What it does |
|---|---|
| `build_anndata/` | raw CellRanger output to the model inputs, 19 notebooks — see `WORKFLOW.md` |
| `combinatorial_perturbations/` | the regression models behind the Figure 5 panels |
| `manuscript_figures/` | the published figure panels, kept as a methods record |

They are grouped under `large_screen/` because a second, smaller screen with
newer data is to be added alongside as `small_screen/`. The two share the
analysis approach but not the data, the module definitions or the cell counts,
so results from one should never be read as results from the other.

## Paths

No notebook here refers to a directory outside this repository. Everything is
either committed beside the notebooks or read from the screen's data root:

| | |
|---|---|
| `paths.py`, `paths.R` | the one definition of `SCREEN_DATA`, `REFERENCE` and `TEXTFILES` |
| `reference/` | small tables the notebooks read, committed, 5 MB |
| `combinatorial_perturbations/RDSFiles/` | the combinatorial fits, committed, 5 MB |
| `build_anndata/TextFiles/` | reference tables build_anndata reads and writes |
| `<repo>/data/large_screen/` | everything large, written by `build_anndata/01`-`19` |

`SCREEN_DATA` defaults to `<repo>/data/large_screen` and the environment
variable `PERTURBDECODE_DATA` overrides it. See `data/README.md`.

Paths between these three folders are relative, so the group moves as a unit.
