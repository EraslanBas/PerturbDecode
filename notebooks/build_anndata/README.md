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

## Requirements

Beyond the PerturbDecode dependencies these notebooks need R with
[DropletUtils](https://bioconductor.org/packages/DropletUtils/) installed, plus
the `[r]` extra:

```bash
pip install 'PerturbDecode[r]'
```

## Where to go next

Once the object exists, the package takes over. See the
[quality control walkthrough](https://perturbdecode.readthedocs.io/en/latest/tutorials/01_quality_control.html)
for the full narrative, including figures from the E3 ligase screen.
