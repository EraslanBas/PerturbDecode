# Data

Nothing in this directory is committed. It is where the notebooks read and
write the screen data, so that no notebook refers to a path outside this
repository.

```
data/
  large_screen/     the E3 ligase screen: what build_anndata/01-19 writes
  small_screen/     the combinatorial screen: what small_screen/01-07 writes
```

A screen's root is resolved by `notebooks/<screen>/paths.py` and `paths.R`. It
defaults to `data/<screen>` here, and an environment variable overrides it —
`PERTURBDECODE_DATA` for the large screen, `PERTURBDECODE_SMALL_DATA` for the
small one:

```bash
export PERTURBDECODE_DATA=/mnt/somewhere/large_screen
```

If the data already exists elsewhere, point at it rather than copying:

```bash
ln -s /path/to/existing/tree data/large_screen
```

## What goes in it

`build_anndata/parameters.py` writes everything here, under the layout its
`par_*` settings describe — `outputs/anndata/`, `outputs/GuideCellLM/` and so
on. Starting from nothing, the raw reads come from
[GEO GSE327057](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE327057)
and `build_anndata/WORKFLOW.md` is the chain that turns them into the rest.

Small reference tables are **not** here: they are committed under
`notebooks/large_screen/reference/`, and the combinatorial fits under
`notebooks/large_screen/combinatorial_perturbations/RDSFiles/`.
