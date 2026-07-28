# 01 · Quality control

:::{admonition} Step 1 of 8: the pipeline walkthrough
:class: tip, dropdown
You are on **step 1**, *Quality control*. See the [full stage list](index.md), or start from the [quickstart](quickstart.md) for the whole pipeline on one page.
:::

## Generating the AnnData object

Everything downstream operates on a single {class}`~anndata.AnnData` object in
which each row is a cell that passed quality control and carries a known
perturbation. Building that object from sequencing output takes four steps:
calling real cells, filtering and merging the channels, resolving which sample
each cell came from, and attaching the guides each cell received.

:::{admonition} This section documents the v1 pipeline
:class: note
These four steps were run with
[PerturbDecode_v1](https://github.com/EraslanBas/PerturbDecode_v1) for the
manuscript and are recorded here as a methods reference. They are not yet part
of the package API, and the figures below come from the full E3 ligase screen.

They also consume per-channel CellRanger output, hashtag demultiplexing results
and feature-barcode tables, which are intermediate files not deposited in GEO.
To follow the walkthrough without rebuilding the object, download the assembled
screen from [GEO GSE327057](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE327057)
and start at [step 03](03_combvae.md). To rebuild it from scratch, start from
the raw reads under BioProject PRJNA1449386.
:::

The E3 ligase screen enters this process as 47 channels across two experimental
rounds and leaves it as one object:

| Step | Operation | Cells |
|---|---|---|
| 1 | Per-channel cell calling | ~21,000 to 28,000 per channel |
| 2 | Filter and concatenate 47 channels | **1,071,671** |
| 3 | Hashtag demultiplexing, singlets only | |
| 4 | Attach guides, drop cells without a confident call | **519,535** |

### Step 1: call real cells in each channel

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
:alt: Barcode rank against UMI count for each of the 47 channels
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

### Step 2: filter and combine the channels

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

This yields **1,071,671 cells by 31,040 genes** across the 47 channels.

### Step 3: resolve which sample each cell came from

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
signal [step 07](07_prediction.md) sets out to predict.

### Step 4: attach the guides

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

The effect is substantial. The guide matrix goes from 1,166,357 cells to 757,147
after the single-read filter, and to 754,450 after the chimeric filter. Joining
against the hash-filtered expression object leaves **519,535 cells**, each with
a confident sample assignment and a confident set of guides.

### Parameters

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

## Next step

::::{grid} 1
:::{grid-item-card} 02 · Guide assignment
:link: 02_guide_assignment
:link-type: doc

Continue the walkthrough.
:::
::::
