# Building the initial AnnData object

These notebooks are **not part of the PerturbDecode package**. They are provided
as a worked example of how to assemble the combined `AnnData` object that the
package takes as its starting point.

They come from the E3 ligase Perturb-seq screen of Geiger-Schuller, Eraslan et al.,
*Systematically characterizing the roles of E3-ligase family members in
inflammatory responses with massively parallel Perturb-seq*, bioRxiv 2023,
[doi:10.1101/2023.01.23.525198](https://doi.org/10.1101/2023.01.23.525198).

The steps here are highly experiment dependent. They reflect the design of the
E3 ligase screen (multiplexed channels, hashtag oligos, a CRISPR feature-barcode
library) and are meant to be read and adapted rather than run unchanged.

## What you need to provide

| File | Purpose |
|---|---|
| `samples.csv` | One row per channel. `sample_name` and `raw` are required; add any other columns you want copied into `.obs` |
| `parameters.py` | Paths and thresholds. Every value is experiment specific |

`samples.csv` columns:

- `h5ad_or_h5_path`: file name of the channel, relative to `par_data_dir`
- `sample_name`: unique identifier for the channel
- `raw`: `True` for unfiltered CellRanger output, which triggers `emptyDrops`
- any further columns, for example `round` and `channel`, are copied to `.obs`

## The notebooks

| Notebook | Does | Skip if |
|---|---|---|
| `01-upstream-qc.ipynb` | Per-channel cell calling with `emptyDrops`, QC metrics, diagnostic plots | never; some form of cell calling is always needed |
| `02-downstream-qc.ipynb` | Per-cell filtering, concatenation of channels, gene filtering | never |
| `03-mergeWithHash.ipynb` | Hashtag demultiplexing, keeping singlets | you did not multiplex with hashing |
| `04-mergeWithCrispr.ipynb` | Attaching guide calls from the feature-barcode table | your guide calls arrive in another format |

Run them in order. Notebook 01 writes `session_01.pkl`, which 02 reads; 02
onwards write the `AnnData` object named by `par_save_filename_1`.

## Reproducing the published analysis

Notebooks 05 to 19 are a different kind of thing from the four above, and it is
worth being explicit about it.

They reproduce the analysis published for the E3 ligase screen. They were
written for that one experiment, before PerturbDecode existed — the package is
what came out of doing this work and finding a more general way to do it. They
are kept here so the published results can be reproduced and checked, not as a
route to follow for a new screen. For a new screen, start from the package at
[quality control](https://perturbdecode.readthedocs.io/en/latest/tutorials/01_quality_control.html).

For that reason they are **not part of the documentation**. The tutorial pages
cover notebooks 01 to 04 and then hand over to the package.

### What they do

They embed and cluster the object, decide which guides worked, estimate each
knockout's effect on each gene, group those effects into modules, and build the
train/test objects the combinatorial models read.

[`WORKFLOW.md`](WORKFLOW.md) lists all nineteen notebooks with what each
produces, and describes the five stages they fall into.

They follow the same conventions as 01 to 04 — `from parameters import *`,
`os.chdir(projectDir)`, every path and threshold in `parameters.py`.

### Running them

`07_AnalyseGuideDepletion` is a diagnostic that nothing downstream reads and
can be skipped.

Four steps take days or longer and are not meant to be rerun: the two guide
fits (10 and 11), the cell selection (14) and the effect-size fit (15). Their
results are provided in `TextFiles/`, each notebook documents how it was
produced, and each writes its own copy under `outputs/` so nothing provided is
overwritten.

Notebook 10 comes in two versions, `_NegativeBinomial` and `_OLS`. Run one, then
set `par_guide_lm_model` to match so notebook 12 reads it. Each writes into its
own subdirectory, so both can be fitted and compared.

Notebooks 10 and 16 are the long ones. The negative binomial fit can be
parallelised by setting `par_guide_block_start` to one guide block per process.
All the fitting notebooks write each block as it completes and skip blocks
already on disk, so an interrupted run resumes.

One further input is not produced by any notebook:
`par_initial_guide_pool_file`, the cells-per-guide composition of the delivered
plasmid pool. It is used only by the diagnostic notebook 07.

### Before you rely on the output

Compare the counts each notebook prints against the numbers in the paper before
treating a result as reproduced. Notebooks 16 to 19 have not been run here at
all.

## Requirements

Beyond the PerturbDecode dependencies these notebooks need R with
[DropletUtils](https://bioconductor.org/packages/DropletUtils/) installed, plus
the `[r]` extra:

```bash
pip install 'PerturbDecode[r]'
```

## Where to go next

Notebooks 01 to 04 are documented step by step, with figures from the E3 ligase
screen, on the
[object generation page](https://perturbdecode.readthedocs.io/en/latest/tutorials/00_data_preparation.html).

Once the object exists, the package takes over at
[quality control](https://perturbdecode.readthedocs.io/en/latest/tutorials/01_quality_control.html).
