"""Tests for package structure, public API and the CLI."""

import subprocess
import sys

import pytest

import perturbdecode


EXPECTED_STEPS = {
    "createTrainValData",
    "runTrainingComBVAE",
    "extract_model_embeddings",
    "visualizePerturbationEmbeddings",
    "selectWorkingGuides",
    "inferEffectSizes",
}


def test_version_is_exposed():
    """The package advertises a version string."""
    assert isinstance(perturbdecode.__version__, str)
    assert perturbdecode.__version__


def test_pipeline_steps_are_importable_callables():
    """Every advertised pipeline step exists at the top level and is callable."""
    assert EXPECTED_STEPS.issubset(set(perturbdecode.pertdec.__all__))
    for name in EXPECTED_STEPS:
        assert callable(getattr(perturbdecode, name)), f"{name} is not callable"


@pytest.mark.parametrize(
    "submodule", ["pertdec", "core", "data", "models", "training", "utils"]
)
def test_submodules_are_accessible(submodule):
    """Each declared submodule is importable from the package root."""
    assert hasattr(perturbdecode, submodule)


def test_r_support_is_optional():
    """The package exposes an R-availability flag and a guard helper."""
    from perturbdecode.utils import libraries

    assert isinstance(libraries.HAS_R, bool)
    assert callable(libraries.require_r)


def test_require_r_raises_when_r_missing(monkeypatch):
    """``require_r`` fails loudly with install instructions when R is absent."""
    from perturbdecode.utils import libraries

    monkeypatch.setattr(libraries, "HAS_R", False)
    with pytest.raises(ImportError, match=r"PerturbDecode\[r\]"):
        libraries.require_r()


def test_cli_version():
    """``perturbdecode --version`` exits cleanly and prints the version."""
    out = subprocess.run(
        [sys.executable, "-m", "perturbdecode.cli", "--version"],
        capture_output=True,
        text=True,
    )
    assert out.returncode == 0
    assert perturbdecode.__version__ in out.stdout


def test_cli_list_steps():
    """``perturbdecode list-steps`` lists every pipeline step."""
    from perturbdecode.cli import main

    assert main(["list-steps"]) == 0


def test_cli_no_args_is_not_an_error():
    """Invoking the CLI with no arguments prints help and succeeds."""
    from perturbdecode.cli import main

    assert main([]) == 0
