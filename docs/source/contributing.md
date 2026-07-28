# Contributing

## Development setup

```bash
git clone https://github.com/EraslanBas/PerturbDecode.git
cd PerturbDecode
pip install -e '.[dev,docs]'
```

## Running the tests

```bash
pytest                        # full suite
pytest --cov=perturbdecode    # with coverage
```

Tests that need R are skipped unless the `[r]` extra is installed.

## Building the docs

```bash
python -m sphinx -b html docs/source docs/_build/html
```

Open `docs/_build/html/index.html`.

## Conventions

- **Docstrings** are NumPy style, rendered by `napoleon`. Every public function
  needs a one-line summary, `Parameters`, and `Returns`.
- **Notebooks** in `docs/source/tutorials/` are committed *with* outputs so the
  site builds without access to real data (`nb_execution_mode = "off"`).
  Elsewhere in the repo, notebook outputs are stripped at commit time by the
  `nbstrip` clean filter.
- **No data files in git.** `.gitignore` uses an allowlist: only recognised
  source and configuration types are tracked.

## Adding a pipeline stage

1. Add the function under `perturbdecode/pertdec/`.
2. Export it from `perturbdecode/pertdec/__init__.py` (`__all__`).
3. Add unit tests using the synthetic fixtures in `tests/conftest.py`.
4. Add it to `docs/source/api/index.rst`.
5. Write the corresponding tutorial page.
