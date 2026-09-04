# 00 · Generating the AnnData object

:::{admonition} Stage 00: before the pipeline
:class: tip, dropdown
You are on **stage 00**, *Generating the AnnData object*. This stage precedes
the pipeline proper and is not part of the package. See the
[full stage list](index.md), or start from the [quickstart](quickstart.md) for
the whole pipeline on one page.
:::

Everything downstream operates on a single {class}`~anndata.AnnData` object in
which each row is a cell that passed quality control and carries a known
perturbation. This stage builds that object; [quality control](01_quality_control.md)
begins once it exists.

That object is never generated in one piece. Droplet capture has a fixed
capacity, so a screen is split across many channels, and larger screens run in
several batches. These have to be combined first, carrying the channel and batch
of origin with them, since batch is a technical source of variation that later
stages account for.

Building the object takes four steps: calling real cells, filtering and merging
the channels, resolving which sample each cell came from, and attaching the
guides each cell received.

:::{important}
**This stage is not the package.** PerturbDecode begins once the combined
`AnnData` object exists. Assembling it is highly experiment dependent, so
rather than impose one procedure, we provide the notebooks used for the E3
ligase screen as a worked example that you can adapt.
:::

## Using these notebooks for your own screen

The four notebooks are in the repository under
[`notebooks/build_anndata/`](https://github.com/EraslanBas/PerturbDecode/tree/main/notebooks/build_anndata).
They run against two files you fill in for your experiment:

- **`samples.csv`**, one row per channel. `sample_name` and `raw` are required;
  any other column you add is copied into `.obs`.
- **`parameters.py`**, holding paths and thresholds. Every value in it is
  experiment specific and must be reviewed before use.

Adapt the steps to your design rather than running all four blindly. The E3
ligase screen multiplexed samples with hashtag oligos and read out guides
through a CRISPR feature-barcode library, so it needs the full sequence. A
screen without hashing skips step 3 entirely; a screen whose guide calls arrive
in a different format replaces step 4 with its own join.

| Notebook | Purpose | Skip it if |
|---|---|---|
| `01-upstream-qc` | Cell calling with `emptyDrops`, QC metrics, diagnostics | never, some form of cell calling is always required |
| `02-downstream-qc` | Per-cell filtering, concatenation, gene filtering | never |
| `03-mergeWithHash` | Hashtag demultiplexing, keeping singlets | you did not multiplex with hashing |
| `04-mergeWithCrispr` | Attaching guide calls from the feature-barcode table | your guide calls arrive in another format |

The figures below come from running these notebooks on the full E3 ligase
screen, described in
[Geiger-Schuller, Eraslan et al., bioRxiv 2023](https://www.biorxiv.org/content/10.1101/2023.01.23.525198v1),
*Systematically characterizing the roles of E3-ligase family members in
inflammatory responses with massively parallel Perturb-seq*.

:::{note}
These steps consume per-channel CellRanger output, hashtag demultiplexing
results and feature-barcode tables. Those are intermediate files, and they are
not deposited in GEO. To follow the rest of the walkthrough without rebuilding
anything, download the assembled screen from
[GEO GSE327057](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE327057)
and continue at [01 · Quality control](01_quality_control.md). To rebuild from
scratch, begin with the raw reads under BioProject PRJNA1449386.
:::

## Step 1: call real cells in each channel

A droplet experiment produces far more barcodes than cells. Most contain only
ambient RNA, and the boundary between an empty droplet and a small or
low-quality cell is not obvious from total counts alone.

Each channel is read separately, annotated with its sample-sheet metadata, and
tested with `emptyDrops` from
[DropletUtils](https://bioconductor.org/packages/DropletUtils/), which compares
each barcode against the ambient profile rather than applying a fixed threshold.
Per-cell QC metrics are computed at the same time.

```python
for sample in sample_sheet.itertuples():
    ad = sc.read_10x_h5(path) if sample.raw else sc.read(path)
    ad.var_names_make_unique()

    # Test each barcode against the ambient RNA profile
    emptydrops(ad, lower=200, niters=10_000, ignore=10, retain=1000)

    ad.obs["n_umis"]  = ad.X.sum(1)
    ad.obs["n_genes"] = (ad.X != 0).sum(1).A1

    # Coarse cutoffs before any per-cell modelling
    ad = ad[ad.obs.n_umis  > 1000]
    ad = ad[ad.obs.n_genes > 300]

    ad.obs["barcode_rank"] = scipy.stats.rankdata(-ad.obs["n_umis"])
    mt = ad.var_names.str.startswith("mt-")
    ad.obs["mt_frac"] = ad.X[:, mt].sum(1).A1 / ad.obs["n_umis"]
```

The barcode-rank curve is the first thing to inspect. Each panel is one channel,
with the two red lines marking the `ignore` and `lower` bounds given to
`emptyDrops`. A healthy channel shows a clear plateau of real cells and a sharp
drop into the ambient population.

```{image} ../_static/figures/qc/barcode_rank.png
:alt: Barcode rank against UMI count for each channel
:width: 100%
```

Total counts against detected genes shows whether the two move together as they
should. Barcodes falling below the diagonal have many reads spread over few
genes, which usually means ambient RNA or a dying cell.

```{image} ../_static/figures/qc/umis_vs_genes.png
:alt: UMIs against detected genes for each channel
:width: 100%
```

The same relationship coloured by `emptyDrops` FDR shows what the test
contributes over a threshold. Points that pass on total counts but score poorly
against the ambient profile are exactly the barcodes a fixed cutoff would keep
by mistake.

```{image} ../_static/figures/qc/umis_vs_genes_emptydrops.png
:alt: UMIs against detected genes coloured by EmptyDrops FDR
:width: 100%
```

The count and gene distributions are worth comparing across channels, since a
channel whose mode sits well away from the others usually indicates a loading or
sequencing-depth problem rather than biology.

::::{grid} 1 2 2 2
:::{grid-item}
```{image} ../_static/figures/qc/umi_distributions.png
:alt: UMI count distributions per channel
```
:::
:::{grid-item}
```{image} ../_static/figures/qc/gene_distributions.png
:alt: Detected gene distributions per channel
```
:::
::::

## Step 2: filter and combine the channels

With cells called, per-cell thresholds are applied and the channels are merged.
The mitochondrial fraction is the informative cut here: a cell whose transcripts
are largely mitochondrial was stressed or dying when captured, and its
expression profile reflects that rather than its perturbation.

```python
for ad in samples.values():
    sc.pp.filter_cells(ad, min_genes=300)
    sc.pp.filter_cells(ad, min_counts=1000)
    ad._inplace_subset_obs(ad.obs.empty_drops_FDR < 0.01)
    ad._inplace_subset_obs(ad.obs.mt_frac < 0.15)
    ad._inplace_subset_var(~ad.var_names.str.startswith("mt-"))

adata = sc.AnnData.concatenate(*samples.values(), join="outer",
                               batch_key="sample_name",
                               batch_categories=list(samples))
sc.pp.filter_genes(adata, min_cells=400)
```

Mitochondrial genes are removed after filtering on them, so that the fraction is
computed from the full transcriptome but the genes themselves do not contribute
to downstream variation. Requiring a gene in at least 400 cells removes those
too rare to estimate an effect on.

## Step 3: resolve which sample each cell came from

Channels are multiplexed, so cells from several samples share a lane and are
separated by hashtag oligos. Demultiplexing assigns each barcode to a sample and
labels doublets, which is the point at which two cells captured together become
detectable.

```python
hash_ad = sc.AnnData.concatenate(*hash_ads.values(),
                                 batch_key="mixhash",
                                 batch_categories=list(hash_ads))

adata.obs["demux_type"]      = hash_ad.obs.demux_type
adata.obs["hash_assignment"] = hash_ad.obs.assignment

adata = adata[adata.obs.demux_type == "singlet"]
```

Only singlets continue. A doublet carries two sets of guides and would appear as
a perturbation combination that was never constructed, which is precisely the
signal [step 04](04_prediction.md) sets out to predict.

## Step 4: attach the guides

The final step joins the feature-barcode table, recording which guides were
detected in each cell. Two filters are applied to the guide counts before the
join.

```python
# A guide seen once is indistinguishable from index hopping
feats = feats.replace(1, 0)
feats = feats[feats.sum(axis=1) > 1]

# Drop guides making up a negligible share of a cell's CRISPR reads
frac = feats.div(feats.sum(axis=1), axis=0)
feats[frac < 0.2] = 0
feats = feats[feats.sum(axis=1) > 0]

adata = adata[adata.obs.index.isin(feats.index)]
adata.obs = adata.obs.join(feats, how="inner")
adata.uns["feature_barcode_names"] = feats.columns.tolist()
```

The first filter discards single-read guide calls, which are as likely to come
from index hopping or ambient guide RNA as from genuine infection. The second
handles chimeric reads: a guide contributing less than 20% of a cell's CRISPR
reads is treated as contamination from another cell rather than as a real
perturbation.

Both filters remove a substantial share of cells. What survives the join
against the hash-filtered expression object is the working object: every cell
with a confident sample assignment and a confident set of guides.

## Parameters

| Parameter | Value | Notes |
|---|---|---|
| `initial_umi_cutoff` | 1000 | Coarse pre-filter before `emptyDrops` |
| `initial_gene_cutoff` | 300 | As above |
| `empty_drops_lower` | 200 | Counts below this define the ambient profile |
| `empty_drops_niters` | 10000 | Monte Carlo iterations; sets the lowest reachable p-value |
| `empty_drops_ignore` | 10 | Barcodes below this are not tested at all |
| `empty_drops_retain` | 1000 | Counts above this are always retained |
| `empty_drops_fdr_cutoff` | 0.01 | Applied at step 2 |
| `cutoff_min_counts` | 1000 | Per-cell, after cell calling |
| `cutoff_min_genes` | 300 | Per-cell |
| `cutoff_min_cells` | 400 | Per-gene |
| `mito_cutoff` | 0.15 | Maximum mitochondrial fraction |
| `crispr_chimeric_reads` | 0.2 | Minimum share of a cell's CRISPR reads for a guide to count |

Raising `mito_cutoff` above roughly 0.2 admits dying cells whose profiles are
dominated by stress response. The chimeric threshold is the parameter to
revisit if a screen shows implausibly many multi-guide cells, since ambient
guide contamination scales with loading density.

## What the finished object must contain

However you assemble it, the object handed to the pipeline has to satisfy the
following contract.

| Location | Field | Type | Required by |
|---|---|---|---|
| `.X` | expression matrix | `float32`, cells × genes | all stages |
| `.obs` | perturbation column | categorical | all stages |
| `.uns` | `"covariates"` | list of `.obs` column names | {class}`~perturbdecode.data.ScreenDataset` |
| `.var` | gene identifiers | index | effect sizes, modules |

### The perturbation column

Perturbation labels must be an **ordered categorical**, and the **first
category is the reference level**, normally your non-targeting controls.
Effect sizes and the model's embedding are both defined relative to it.

```python
import pandas as pd

categories = ["control", "KO_A", "KO_B"]   # control first
adata.obs["perturbation"] = pd.Categorical(
    adata.obs["perturbation"], categories=categories, ordered=True
)
```

:::{warning}
Getting the reference level wrong silently changes the meaning of every
downstream effect size. Check `adata.obs["perturbation"].cat.categories[0]`
before proceeding.
:::

### Covariates

`ScreenDataset` reads the covariate columns it should one-hot encode from
`.uns["covariates"]`:

```python
adata.uns["covariates"] = ["perturbation"]
```

The reference level is dropped from the one-hot encoding, so a screen with
*k* perturbation levels contributes *k − 1* covariate columns.

### Normalisation

<!-- TODO: state the expected normalisation. The ComBVAE reconstruction loss is
     MSE, which implies log-normalised (not raw count) input. Confirm against
     the E3Ligase preprocessing notebooks and document the exact recipe. -->

### Checking your object

```python
assert adata.uns.get("covariates"), "set adata.uns['covariates']"
assert adata.obs["perturbation"].dtype.name == "category"
print("reference level:", adata.obs["perturbation"].cat.categories[0])
```

<!-- TODO: short recipes for converting common formats: CellRanger output, a
     Seurat object via anndata2ri, and a plain counts matrix + metadata table. -->

## Next step

::::{grid} 1
:::{grid-item-card} 01 · Quality control
:link: 01_quality_control
:link-type: doc

Continue the walkthrough.
:::
::::
