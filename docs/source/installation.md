# Installation

## Requirements

- Python ≥ 3.8
- A working PyTorch install (CPU is sufficient for the tutorials; a GPU is
  recommended for training ComBVAE on a full screen)

## From PyPI

```bash
pip install PerturbDecode
```

The distribution is named **`PerturbDecode`**; the import name is
**`perturbdecode`**.

```python
import perturbdecode as pd
print(pd.__version__)
```

## Optional extras

::::{tab-set}

:::{tab-item} R integration
Some steps (effect-size processing, module identification) call into R.

```bash
pip install 'PerturbDecode[r]'
```

This installs `rpy2` and `anndata2ri`. The core package works without them;
steps that need R raise an `ImportError` with installation instructions.
:::

:::{tab-item} Development
```bash
git clone https://github.com/EraslanBas/PerturbDecode.git
cd PerturbDecode
pip install -e '.[dev]'
pytest
```
:::

:::{tab-item} Documentation
```bash
pip install -e '.[docs]'
python -m sphinx -b html docs/source docs/_build/html
```
:::

::::

## Verifying the installation

```bash
perturbdecode --version
perturbdecode list-steps
```

Or run the bundled smoke test, which builds a synthetic screen and runs a
forward pass through the model. No real data is required:

```bash
python examples/python_example.py
```

## Troubleshooting

:::{dropdown} `OSError: Could not load shared object file: libllvmlite.so`
:color: warning
:icon: alert

Seen on conda installations whose **system** `libstdc++.so.6` is older than the
one conda ships. Importing `torch` before `scanpy` binds the system library,
which then lacks the `GLIBCXX` version `numba`/`llvmlite` requires.

Put conda's library directory first on the loader path:

```bash
export LD_LIBRARY_PATH="$CONDA_PREFIX/lib:$LD_LIBRARY_PATH"
```

Add it to your shell profile to make it permanent. As a workaround, importing
`perturbdecode` (or `scanpy`) *before* `torch` also avoids the problem.
:::

:::{dropdown} `ImportError: ... requires the optional R dependencies`
:icon: info

The step you called needs the R extra:

```bash
pip install 'PerturbDecode[r]'
```

You also need a working R installation on the system for `rpy2` to bind to.
:::
