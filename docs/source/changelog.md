# Release notes

## 0.1.0 (unreleased)

First packaged release.

### Added
- Installable package `PerturbDecode` (import name `perturbdecode`).
- Command-line interface: `perturbdecode --version`, `perturbdecode list-steps`.
- Six pipeline steps exposed at the package root: `createTrainValData`,
  `selectWorkingGuides`, `inferEffectSizes`, `runTrainingComBVAE`,
  `extract_model_embeddings`, `visualizePerturbationEmbeddings`.
- Test suite covering model shapes, loss behaviour, gradient flow, the public
  API surface, the CLI and the R bridge.
- Documentation site.

### Changed
- R support (`rpy2`, `anndata2ri`) is now an optional `[r]` extra rather than a
  hard requirement of every import.

### Notes
- The L1 penalty on the perturbation embedding present in earlier versions of
  the model code was computed but never added to the optimised loss, so it did
  not affect training. The packaged model omits it.
