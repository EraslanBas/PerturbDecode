# Large screen

The E3 ligase Perturb-seq screen of Geiger-Schuller, Eraslan et al.,
*Systematically characterizing the roles of E3-ligase family members in
inflammatory responses with massively parallel Perturb-seq*,
[doi:10.1101/2023.01.23.525198](https://doi.org/10.1101/2023.01.23.525198).

It is a **family-focused** screen, not a genome-wide one: the paper interrogates
"the function of 1,130 E3 ligases, partners and substrates in the inflammatory
response in primary dendritic cells". The tables in this repository agree —
1,130 target genes, 3,719 guides in the delivered pool, 242,938 cells surviving
selection. "Large" here means large relative to the combinatorial screen in
`../small_screen/`, which perturbs 14 genes.

| Folder | What it does |
|---|---|
| `build_anndata/` | raw CellRanger output to the model inputs, 19 notebooks — see `WORKFLOW.md` |
| `manuscript_figures/` | the published figure panels, kept as a methods record |
| `combinatorial_perturbations/` | the regression models behind the Figure 5 panels |
| `ica_factorisation/` | the 15-component decomposition of the effect-size matrix, and how 15 was chosen |
| `revision_analyses/` | the knockout modules against the DC subtypes, and two robustness checks |

The combinatorial screen sits alongside as `../small_screen/`. The two share
the module definitions, which the small screen reads from this one, but not the
data, the guide set or the cell counts — so a result from one should never be
read as a result from the other.

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
